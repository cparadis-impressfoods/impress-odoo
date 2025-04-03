# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class QuantHistoryGroup(models.Model):
    _name = "warehouse.quant.group"
    _description = "Quant History Group"

    name = fields.Char("Name")
    partner_id = fields.Many2one("res.partner", "Customer")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    config_id = fields.Many2one(
        "warehouse.billing.config", string="Billing Configuration"
    )
    quant_history_ids = fields.One2many(
        "warehouse.quant.history", "group_id", string="Quant History"
    )

    invoicing_state = fields.Selection(
        [
            ("not_invoiced", "Not Invoiced"),
            ("partially_invoiced", "Partially Invoiced"),
            ("invoiced", "Invoiced"),
        ],
        string="Invoicing State",
        compute="_compute_invoicing_state",
        store=True,
    )

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", related="sale_order_line_id.order_id"
    )
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")

    invoiced = fields.Boolean(
        string="Invoiced", default=False, compute="_compute_invoiced", store=True
    )
    invoice_ids = fields.Many2many(
        "account.move", string="Invoice Reference", related="sale_order_id.invoice_ids"
    )

    @api.depends("quant_history_ids", "quant_history_ids.invoiced", "sale_order_id")
    def _compute_invoicing_state(self):
        for record in self:
            if record.quant_history_ids:
                if all(history.invoiced for history in record.quant_history_ids):
                    record.invoicing_state = "invoiced"
                elif any(history.invoiced for history in record.quant_history_ids):
                    record.invoicing_state = "partially_invoiced"
                else:
                    record.invoicing_state = "not_invoiced"
            else:
                record.invoicing_state = "not_invoiced"

    @api.depends("sale_order_line_id", "sale_order_line_id.invoice_status")
    def _compute_invoiced(self):
        for record in self:
            if (
                record.sale_order_line_id
                and record.sale_order_line_id.invoice_status == "invoiced"
            ):
                record.invoiced = True
                for line in record.quant_history_ids:
                    if not line.invoice_id:
                        line.write({"invoice_id": self.invoice_ids[0].id})
            else:
                record.invoiced = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("warehouse.usage.group") or "/"
                )
        return super(QuantHistoryGroup, self).create(vals_list)

    def get_usage(self) -> float:
        self.ensure_one()
        match self.config_id.measurement_type:
            case "cubic":
                return sum(r.get_volume() for r in self.quant_history_ids)
            case "square":
                return sum(r.get_area() for r in self.quant_history_ids)
            case "pallet":
                return sum(r.get_pallet_qty() for r in self.quant_history_ids)
            case _:
                return 0.0

    def action_linked_sale_order(self):
        self.ensure_one()
        action = {
            "res_model": "sale.order",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
        }

        return action

    def action_linked_invoices(self):
        self.ensure_one()
        return self.sale_order_id.action_view_invoice()

    def generate_sale_order_line_values(self):
        self.ensure_one()

        records = self.quant_history_ids

        # Calculate total
        total_amount = 0
        measurement_type = self.config_id.measurement_type
        rate = self.config_id.rate

        # Calculate total usage
        if measurement_type == "cubic":
            total_usage = sum(r.get_volume() for r in records)
            uom = "m³"
        elif measurement_type == "square":
            total_usage = sum(r.get_area() for r in records)
            uom = "m²"
        else:  # pallet
            total_usage = sum(r.get_pallet_qty() for r in records)
            uom = "pallets"

        total_usage = total_usage + self.config_id.base_qty
        total_amount = total_usage * rate + self.config_id.flat_fee

        date_from, date_to = self.date_from, self.date_to

        description = _(
            f"""Warehouse Space Usage: {date_from} to {date_to}\n"""
            f"""Category: {self.config_id.name}\n"""
            f"""Cycle: {self.config_id.billing_cycle}\n"""
            f"""Total Usage: {total_usage} {uom}\n"""
            f"""Rate: {rate:.2f} per {uom}"""
        )

        sale_order_line_vals = {
            "product_id": self.config_id.billing_product_id.id,
            "name": description,
            "product_uom_qty": 1,
            "price_unit": total_amount,
            "currency_id": self.config_id.currency_id.id,
        }
        return sale_order_line_vals

    @api.model
    def group_quant_history(self, config, today):

        domain = []
        domain += config.get_filter_domain()
        dates = config.get_billing_dates(today)
        domain += [("date", ">=", dates[0]), ("date", "<=", dates[1])]

        # First, check if a quant_group already exists for the given dates and config

        existing_group = self.env["warehouse.quant.group"].search(
            [
                ("date_from", "=", dates[0]),
                ("date_to", "=", dates[1]),
                ("config_id", "=", config.id),
                ("partner_id", "=", config.partner_id.id),
            ]
        )

        # Here, the domain should be the one from the warehouse.billing.config
        quant_history = self.env["warehouse.quant.history"]
        domain = config.get_filter_domain() + [("usage_group_id", "=", False)]
        records = quant_history.search(domain)

        if existing_group and len(existing_group) == 1:
            existing_group.write(
                {
                    "quant_history_ids": [
                        (fields.Command.link(record.id)) for record in records
                    ],
                }
            )
            return existing_group
        elif existing_group and len(existing_group) > 1:
            raise ValidationError(
                _(
                    "Multiple quant groups found for the same dates and configuration. Please delete the duplicates and try again."
                )
            )

        # If no records are found, return an empty recordset and do not create an empty quant_group
        if not records:
            return self.env["warehouse.quant.group"]
        else:
            return self.env["warehouse.quant.group"].create(
                {
                    "quant_history_ids": [
                        (fields.Command.link(record.id)) for record in records
                    ],
                    "date_from": dates[0],
                    "date_to": dates[1],
                    "config_id": config.id,
                    "partner_id": config.partner_id.id,
                }
            )
