import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MaintenanceStage(models.Model):
    _inherit = "maintenance.stage"

    color = fields.Integer(string="Color", default="1")
