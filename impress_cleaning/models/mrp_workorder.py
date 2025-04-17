from datetime import datetime

from odoo import _, models


class MrpProductionWorkcenterLine(models.Model):
    _inherit = "mrp.workorder"

    def action_request_cleaning(self):
        self.ensure_one()
        action = {
            "name": _("New Cleaning Request"),
            "view_mode": "form",
            "views": [
                (
                    self.env.ref(
                        "mrp_maintenance.maintenance_request_view_form_inherit_mrp_workorder"
                    ).id,
                    "form",
                )
            ],
            "res_model": "maintenance.request",
            "type": "ir.actions.act_window",
            "context": {
                "default_company_id": self.company_id.id,
                "default_workorder_id": self.id,
                "default_production_id": self.production_id.id,
                "discard_on_footer_button": True,
                "default_maintenance_type": "cleaning",
                "default_schedule_date": datetime.today(),
                "default_name": "Cleaning - " + self.workcenter_id.name,
                "default_duration": (
                    0.5
                    if self.workcenter_id.cleaning_time == 0
                    else self.workcenter_id.cleaning_time
                ),
                "default_maintenance_for": "workcenter",
                "default_workcenter_id": self.workcenter_id.id,
                "default_maintenance_team_id": self.workcenter_id.cleaning_team_id.id,
                "default_user_id": self.workcenter_id.cleaning_user_id.id,
                "default_description": f"""
                    Cleaning after {self.product_id.display_name}
                """,
            },
            "target": "new",
            "domain": [("workorder_id", "=", " self")],
        }
        return action
