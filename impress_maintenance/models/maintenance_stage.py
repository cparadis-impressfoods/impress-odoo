# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MaintenanceStage(models.Model):
    _inherit = "maintenance.stage"

    color = fields.Integer(string="Color", default="1")
