import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_view_warehousing_fees(self):
        self.ensure_one()
        action = {
            "res_model": "warehouse.billing.config",
            "type": "ir.actions.act_window",
        }

        configs = self.env["warehouse.billing.config"].search(
            [("partner_id", "=", self.id)]
        )

        if len(configs) == 1:
            action.update({"view_mode": "form", "res_id": configs[0].id})  # type: ignore

        else:
            action.update(
                {
                    "name": _("Warehousing Rules for %s", self.name),
                    "domain": [("partner_id", "=", self.id)],
                    "view_mode": "tree,form",
                }
            )  # type: ignore

        return action
