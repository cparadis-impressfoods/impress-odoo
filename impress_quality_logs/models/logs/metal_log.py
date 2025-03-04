# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
_logger = logging.getLogger(__name__)


class MetalLog(models.Model):
    _inherit = 'log.mixin'
    _name = "metal.log"
    _description = "Metal Detector Log"

    log_line_ids = fields.One2many(comodel_name='metal.log.line', inverse_name='metal_log_id')
    monthly_signature = fields.Binary('Monthly Signature')
    monthly_signature_date = fields.Datetime('Monthly Signature Date', compute='_compute_monthly_signature_date', store=True)


    @api.depends("monthly_signature")
    def _compute_monthly_signature_date(self):
        for rec in self:
            rec.monthly_signature_date = datetime.now()
    def action_view_metal_lines(self):
        self.ensure_one()
        action = {
            'res_model': 'metal.log.line',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'domain': [('metal_log_id','=', self.id)],
        }
        return action