import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    color = fields.Integer(string="Color", default="1")
