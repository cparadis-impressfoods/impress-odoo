# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Xray_log_line(models.Model):
    _inherit = 'log_line.mixin'
    _name = 'x_ray_log_line'
    reject_value = fields.Integer('Reject Value')
    
    stainless_detection_value = fields.Integer('Stainless Detection Value')
    ceramic_detection_value = fields.Integer('Ceramic Detection Value')
    glass_detection_value = fields.Integer('Glass Detection Value')

    ejection = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Calibration')
    last_check_for_product = fields.Boolean('Last check for product')
    
    total_qty = fields.Integer('Total Quantity')
    reject_qty = fields.Integer('Reject Quantity')
    average = fields.Integer('Average')
