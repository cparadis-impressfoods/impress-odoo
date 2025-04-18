from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"
    _name = "maintenance.request"

    maintenance_type = fields.Selection(
        selection_add=[("cleaning", "Cleaning")],
        default="corrective",
    )
