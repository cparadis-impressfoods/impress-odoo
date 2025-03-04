# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
_logger = logging.getLogger(__name__)


class Xray_log(models.Model):
    _name="x_ray.log"
    _inherit="log.mixin"
    _description = 'X-Ray Detector Log'

    log_line_ids = fields.One2many(comodel_name='x_ray.log.line', inverse_name='x_ray_log_id')

    average_threshold = fields.Integer('Average Threshold')

    monthly_signature = fields.Binary('Monthly Signature')
    monthly_signature_date = fields.Datetime('Monthly Signature Date', compute='_compute_monthly_signature_date', store=True)



    @api.depends('monthly_signature')
    def _compute_monthly_signature_date(self):
        for rec in self:
            rec.monthly_signature_date = datetime.now()

    def action_view_x_ray_lines(self):
        self.ensure_one()
        action = {
            'res_model': 'x_ray.log.line',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'domain': [('x_ray_log_id', '=', self.id)],
        }
        return action