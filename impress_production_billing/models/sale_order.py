import logging
from collections import defaultdict

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    linked_production_ids = fields.One2many(
        "mrp.production",
        "billing_sale_order_id",
        string="Linked Productions",
        copy=False,
    )
    linked_production_count = fields.Integer(
        "Count of linked MOs", compute="_compute_linked_production_ids"
    )

    @api.depends("linked_production_ids")
    def _compute_linked_production_ids(self):
        for rec in self:
            rec.linked_production_count = len(rec.linked_production_ids)

    def action_view_linked_productions(self):
        self.ensure_one()
        action = {
            "res_model": "mrp.production",
            "type": "ir.actions.act_window",
        }
        if len(self.linked_production_ids) == 1:
            action.update(
                {
                    "view_mode": "form",
                    "res_id": self.linked_production_ids.id,
                }  # type: ignore
            )

        else:
            action.update(
                {
                    "name": _("Manufacturing Orders Generated by %s", self.name),
                    "domain": [("id", "in", self.linked_production_ids.ids)],
                    "view_mode": "tree,form",
                }  # type: ignore
            )

        return action

    def portal_get_productions_grouped(self):
        self.ensure_one()
        productions = self.linked_production_ids
        productions_grouped = defaultdict(lambda: [])
        for production in productions:
            productions_grouped[production.product_id].append(production)

        values = []
        for product in productions_grouped:
            values.append(
                (product.id, product.display_name, len(productions_grouped[product]))
            )

        return values
