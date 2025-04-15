import logging
from datetime import datetime
from math import ceil

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class QuantHistory(models.Model):
    _name = "warehouse.quant.history"
    _description = "Quant History"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product", string="Product")
    date = fields.Date(string="Date")
    quantity = fields.Float(string="Quantity")
    location_id = fields.Many2one("stock.location", string="Location")
    warehouse_id = fields.Many2one(
        "stock.warehouse", related="location_id.warehouse_id"
    )
    lot_id = fields.Many2one("stock.lot", string="Lot")
    group_id = fields.Many2one("warehouse.quant.group", string="Quant History Group")
    quant_id = fields.Integer(string="Quant ID")

    invoice_id = fields.Many2one("account.move", string="Invoice")
    invoiced = fields.Boolean(
        string="Invoiced",
        compute="_compute_invoiced",
    )

    @api.depends("invoice_id")
    def _compute_invoiced(self):
        for record in self:
            _logger.info(record.invoice_id)
            if record.invoice_id:
                record.invoiced = True
            else:
                record.invoiced = False

    def get_pallet_qty(self) -> int:
        if not self.product_id.qty_per_pallet:
            raise UserError(_("Product does not have a quantity per pallet"))
        return ceil(self.quantity / self.product_id.qty_per_pallet)

    def get_volume(self) -> float:
        return self.product_id.volume * self.quantity  # type: ignore

    def get_area(self) -> float:
        raise ValidationError(_("Not Implemented"))
        return 0.0

    @api.model
    def create_from_quant(self, quants, day=datetime.today()):
        vals = []

        for quant in quants:
            if (
                len(
                    self.env["warehouse.quant.history"].search(
                        [("quant_id", "=", quant.id), ("date", "=", day)]
                    )
                )
                > 0
            ):
                continue
            vals.append(
                {
                    "quant_id": quant.id,
                    "product_id": quant.product_id.id,
                    "date": day,
                    "quantity": quant.quantity,
                    "location_id": quant.location_id.id,
                    "warehouse_id": quant.location_id.warehouse_id.id,
                    "lot_id": quant.lot_id.id,
                }
            )

        return self.create(vals)
