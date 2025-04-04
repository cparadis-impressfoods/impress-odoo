# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class QualityAlert(models.Model):
    _inherit = "quality.alert"

    maintenance_request_id = fields.Many2one(
        "maintenance.request", "Maintenance Request"
    )
