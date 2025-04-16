import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    notes = fields.Text(string="Notes")
    state_color = fields.Integer(string="State Color", related="stage_id.color")
    employee_color = fields.Integer(
        string="Employee Color", related="assigned_employee.color"
    )
    assigned_employee = fields.Many2one(
        comodel_name="hr.employee",
        string="Assigned Employee",
    )

    def create(self, vals_list):
        # self._move_weekend(vals_list)
        return super().create(vals_list)

    @api.model
    def _move_weekend(self, vals):
        if "schedule_date" in vals and vals["schedule_date"]:
            full_date: datetime = vals.get("schedule_date")
            date = full_date.date().timetuple()
            match date.tm_wday:
                case 5:
                    vals["schedule_date"] = full_date + timedelta(days=2)
                case 6:
                    vals["schedule_date"] = full_date + timedelta(days=1)

        return vals
