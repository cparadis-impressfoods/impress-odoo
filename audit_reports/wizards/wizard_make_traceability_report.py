import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class WizardMakeTraceabilityReport(models.TransientModel):
    _name = "wizard.make.traceability.report"
    _description = _("WizardMakeTraceabilityReport")

    name = fields.Char(_("Name"))
    show_full_traceability = fields.Boolean(
        string="Show Full Traceability", default=False
    )
    show_client_list = fields.Boolean(string="Show Client List", default=False)
    show_product_list = fields.Boolean(string="Show Product List", default=False)

    def add(self):
        report = self.env["lot.audit.report"].create(
            {
                "lot_id": self.env.context.get("active_id"),
                "show_full_traceability": self.show_full_traceability,
                "show_client_list": self.show_client_list,
                "show_product_list": self.show_product_list,
            }
        )
        return report.action_create_report()
