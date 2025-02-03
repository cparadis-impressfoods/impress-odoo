# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CodingLog(models.Model):
    _inherit = 'log.mixin'
    _name = 'coding.log'
    _description = 'Coding Log'

    log_line_ids = fields.One2many(comodel_name='coding.log.line', inverse_name='coding_log_id')

    def action_view_coding_lines(self):
        self.ensure_one()
        action = {
            'res_model': 'coding.log.line',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'domain': [('coding_log_id', '=', self.id)],
        }
        return action