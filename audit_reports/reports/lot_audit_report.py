# -*- coding: utf-8 -*-
from typing import Mapping, Iterable
import logging

from odoo import models, fields, api
from odoo.addons.stock.models.stock_lot import StockLot
from odoo.addons.stock.models.stock_move_line import StockMoveLine
from odoo.addons.mrp.models.mrp_production import MrpProduction

_logger = logging.getLogger(__name__)


class LotAuditReport(models.TransientModel):
    _name = "lot.audit.report"
    _description = "Lot Audit Report"

    lot_id = fields.Many2one("stock.lot", string="Lot", required=True)
    product_id = fields.Many2one(
        "product.product", string="Product", related="lot_id.product_id"
    )

    show_full_traceability = fields.Boolean(
        string="Show Full Traceability", default=False
    )
    show_client_list = fields.Boolean(string="Show Client List", default=False)
    show_product_list = fields.Boolean(string="Show Product List", default=False)

    def get_total_produced(self):
        lines: StockMoveLine = self._get_lines(self.lot_id)
        production_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "mo_in"
        )

        returned_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "unbuild"
        )

        quantity = sum(production_lines.mapped("quantity")) - sum(
            returned_lines.mapped("quantity")
        )

        return quantity

    def get_total_bought(self):
        lines: StockMoveLine = self._get_lines(self.lot_id)
        purchase_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "purchase"
        )
        return sum(purchase_lines.mapped("quantity"))

    def get_total_delivered(self):
        lines: StockMoveLine = self._get_lines(self.lot_id)
        delivery_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "sale"
        )
        returned_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "return_in"
        )

        quantity = sum(delivery_lines.mapped("quantity")) - sum(
            returned_lines.mapped("quantity")
        )

        return -1 * quantity

    def get_total_used(self):
        lines: StockMoveLine = self._get_lines(self.lot_id)
        used_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "mo_out"
        )
        return -1 * sum(used_lines.mapped("quantity"))

    def get_total_unbuild(self):
        lines: StockMoveLine = self._get_lines(self.lot_id)
        unbuild_lines: StockMoveLine = lines.filtered(
            lambda line: self._get_sml_type(line) == "unbuild"
        )
        return -1 * sum(unbuild_lines.mapped("quantity"))

    def get_all_deliveries(self) -> StockMoveLine:
        audit = self.get_all_downstream_moves(self.lot_id)
        delivery_lines: StockMoveLine = self.env["stock.move.line"]

        for lot in audit:
            if "delivery" in audit[lot]:
                delivery_lines += audit[lot]["delivery"]
        return delivery_lines

    def get_client_recalls(self):
        deliveries = self.get_all_deliveries()
        return deliveries.grouped(lambda line: line.move_id.picking_id.partner_id)

    def get_product_recalls(self):
        deliveries = self.get_all_deliveries()
        deliveries_grouped = deliveries.grouped(lambda line: line.move_id.product_id)
        data = {}

        for product in deliveries_grouped:
            grouped_by_lots = deliveries_grouped[product].grouped(
                lambda line: line.lot_id
            )
            for lot in grouped_by_lots:
                data[product] = [lot, sum(grouped_by_lots[lot].mapped("quantity"))]
        return data

    def action_create_report(self):
        return self.env.ref("audit_reports.report_lot_audit").report_action(self.id)

    @api.model
    def _get_lines(self, lot_id):
        move_line = self.env["stock.move.line"]
        lines = move_line.search(
            [
                ("lot_id", "=", lot_id.id),
                ("state", "=", "done"),
            ]
        )
        return lines

    @api.model
    def is_mapping(self, value):
        return isinstance(value, Mapping)

    @api.model
    def is_iterable(self, value):
        return isinstance(value, Iterable)

    @api.model
    def is_string(self, value):
        return isinstance(value, str)

    @api.model
    def _get_sml_type(self, value: StockMoveLine) -> str:
        sm = value.move_id
        if sm.picking_id:
            match sm.picking_code:
                case "outgoing":
                    return "delivery"
                case "incoming":
                    if sm.picking_id.return_id:
                        return "delivery_return"
                    else:
                        return "purchase"
                case _:
                    _logger.warning("Unknown picking type: %s", sm.picking_code)
                    return ""
        elif sm.purchase_line_id:
            return "purchase"
        elif sm.sale_line_id:
            return "sale"
        elif sm.scrap_id:
            return "scrap"
        elif sm.production_id:
            return "mo_in"
        elif sm.raw_material_production_id:
            return "mo_out"
        elif sm.unbuild_id:
            return "unbuild"
        else:
            return "internal"

    @api.model
    def get_sml_type_display_name(self, value: str) -> str:
        match value:
            case "mo_out":
                return "Used in Production"
            case "mo_in":
                return "Produced"
            case "delivery":
                return "Delivery"
            case "purchase":
                return "Purchase"
            case "sale":
                return "Sale"
            case "unbuild":
                return "Unbuild"
            case "delivery_return":
                return "Return"
            case _:
                return value

    @api.model
    def get_sml_qty(self, value: StockMoveLine) -> float:
        type = self._get_sml_type(value)
        out_types = ["mo_out", "sale", "delivery", "scrap", "unbuild"]

        if type in out_types:
            return -1 * value.quantity  # type: ignore
        else:
            return value.quantity  # type: ignore

    @api.model
    def get_name(self, value):

        if isinstance(value, StockMoveLine):
            match self._get_sml_type(value):  # type: ignore
                case "purchase":
                    return value.move_id.purchase_line_id.order_id.display_name  # type: ignore
                case "sale":
                    return value.move_id.sale_line_id.order_id.display_name  # type: ignore
                case "scrap":
                    return value.move_id.scrap_id.display_name  # type: ignore
                case "delivery":
                    return f"{value.move_id.picking_id.display_name}"  # type: ignore
                case "mo_in":
                    return f"{value.move_id.production_id.display_name}"  # type: ignore
                case "mo_out":
                    return f"{value.move_id.raw_material_production_id.display_name}"  # type: ignore
                case "unbuild":
                    return f"{value.move_id.unbuild_id.display_name}"  # type: ignore
                case "delivery_return":
                    return f"{value.move_id.picking_id.display_name}"  # type: ignore
                case _:
                    return f"{value.move_id.display_name} ({value.quantity} {value.product_uom_id.display_name})"  # type: ignore
        elif isinstance(value, MrpProduction):
            return f"{value.name} - {value.product_id.display_name} - {value.lot_producing_id.display_name}"  # type: ignore
        elif isinstance(value, StockLot):
            return f"{value.product_id.display_name} - {value.display_name}"  # type: ignore
        elif isinstance(value, models.Model):
            return value.display_name
        elif isinstance(value, str):
            return value
        else:
            return "NA"

    @api.model
    def get_add_info(self, value: StockMoveLine) -> str:
        match self._get_sml_type(value):
            case "mo_in":
                return value.move_id.production_id.product_id.display_name
            case "mo_out":
                return value.move_id.raw_material_production_id.product_id.display_name
            case "sale":
                return value.move_id.sale_line_id.order_id.partner_id.display_name
            case "purchase":
                return value.move_id.purchase_line_id.order_id.partner_id.display_name
            case "delivery":
                return value.move_id.picking_id.partner_id.display_name
            case "unbuild":
                return value.move_id.unbuild_id.mo_id.display_name
            case "delivery_return":
                return value.move_id.picking_id.return_id.display_name
            case _:
                return ""

    @api.model
    def get_all_downstream_moves(self, lot_id: StockLot, max_depth: int = 0):
        if not lot_id or len(lot_id) == 0:
            return {}

        lot_queue: list[StockLot] = [lot_id]
        audit: dict[StockLot, dict[str, StockMoveLine]] = {}
        current_depth: int = 1
        while len(lot_queue) > 0 and (current_depth <= max_depth or max_depth == 0):
            lot = lot_queue.pop(0)
            grouped_lines = self._get_lines(lot).grouped(self._get_sml_type)
            audit[lot] = grouped_lines
            if "mo_out" in grouped_lines:
                for line in grouped_lines["mo_out"]:
                    lot_queue.append(
                        line.move_id.raw_material_production_id.lot_producing_id
                    )
            current_depth += 1
        return audit

    @api.model
    def get_audit_tree(self, lot_id: StockLot):
        if not lot_id or len(lot_id) == 0:
            return {}

        # _logger.warning(f"Building audit tree for lot {lot_id.product_id.name}-{lot_id.name}")
        sml = self.env["stock.move.line"]

        audit = {
            "Lot": lot_id,
            "Receptions": sml,
            "Inventory Adjustments In": sml,
            "Unbuild In": sml,
            "MO Where Produced": sml,
            "Returns In": sml,
            "inventory_adjustments_out": sml,
            "Unbuild Out": sml,
            "Deliveries": sml,
            "Scrap": sml,
            "Used In": {},
        }

        lines = sml.search([("lot_id", "=", lot_id.id)])

        # Qty In

        # Receptions
        reception_lines = lines.filtered_domain(
            [("move_id.purchase_line_id", "!=", False)]
        )
        audit["Receptions"] += reception_lines

        # Inventory adjustments in
        inventory_adjustment_lines_in = lines.filtered_domain(
            [
                ("move_id.production_id", "=", False),  # No sml related to productions
                (
                    "move_id.raw_material_production_id",
                    "=",
                    False,
                ),  # No sml related to productions
                ("move_id.picking_id", "=", False),  # No sml related to pickings
                ("move_id.purchase_line_id", "=", False),  # No sml related to purchases
                ("move_id.sale_line_id", "=", False),  # No sml related to sales
                ("move_id.scrap_id", "=", False),  # No sml related to scrap
                ("move_id.unbuild_id", "=", False),  # No sml related to unbuilds
                ("location_dest_usage", "=", "internal"),
            ]
        )

        audit["Inventory Adjustments In"] += inventory_adjustment_lines_in

        # Unbuild in TODO: Figure out how to distinguish between unbuild in and out
        unbuild_in_lines = lines.filtered_domain([("move_id.unbuild_id", "!=", False)])
        audit["Unbuild In"] += unbuild_in_lines

        # MO in
        production_in_lines = lines.filtered_domain(
            [("move_id.production_id", "!=", False)]
        )
        audit["MO Where Produced"] += production_in_lines

        # Returns in
        returns_in = lines.filtered_domain(
            [
                ("location_usage", "=", "customer"),
                ("location_dest_usage", "=", "internal"),
            ]
        )
        audit["Returns In"] += returns_in

        # Qty Out

        # MO out
        production_out_lines = lines.filtered_domain(
            [("move_id.raw_material_production_id", "!=", False)]
        )
        audit["Used In"] = {
            mo: self.get_audit_tree(mo.mapped("lot_producing_id"))
            for mo in production_out_lines.mapped("move_id.raw_material_production_id")
        }

        # Inventory adjustments out
        inventory_adjustment_lines_out = lines.filtered_domain(
            [
                ("move_id.production_id", "=", False),  # No sml related to productions
                (
                    "move_id.raw_material_production_id",
                    "=",
                    False,
                ),  # No sml related to productions
                ("move_id.picking_id", "=", False),  # No sml related to pickings
                ("move_id.purchase_line_id", "=", False),  # No sml related to purchases
                ("move_id.sale_line_id", "=", False),  # No sml related to sales
                ("move_id.scrap_id", "=", False),  # No sml related to scrap
                ("move_id.unbuild_id", "=", False),  # No sml related to unbuilds
                ("location_dest_usage", "!=", "internal"),
            ]
        )

        audit["inventory_adjustments_out"] += inventory_adjustment_lines_out

        # Unbuild out TODO: Figure out how to distinguish between unbuild in and out
        unbuild_out_lines = lines.filtered_domain([("move_id.unbuild_id", "!=", False)])
        audit["Unbuild Out"] += unbuild_out_lines

        # Scrap
        scrap_lines = lines.filtered_domain([("move_id.scrap_id", "!=", False)])
        audit["Scrap"] += scrap_lines

        # Deliveries
        delivery_lines = lines.filtered_domain(
            [("location_dest_usage", "=", "customer")]
        )
        audit["Deliveries"] += delivery_lines

        return audit
