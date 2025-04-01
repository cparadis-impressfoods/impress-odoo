# -*- coding: utf-8 -*-
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    notes = fields.Text(string="Notes")
    technician_id = fields.Many2one("hr.employee", string="Technician")
