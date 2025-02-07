# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CodingLog(models.Model):
    _inherit = 'log.mixin'
    _name = 'coding.log'
    _description = 'Coding Log'

    #log_line_ids = fields.One2many(comodel_name='coding.log.line', inverse_name='coding_log_id')
    case_code = fields.Char('Case Code')
    unit_code = fields.Char('Unit Code')

    notes = fields.Char('Notes')
    start_date = fields.Datetime('Start Date')

    unit_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Unit Check')
    sleeve_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Sleeve Check')
    case_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Case Check')
    subunit_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Subunit Check')
    shelf_life_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Shelf Life Check')
    keep_cold_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Keep Cold Check')

    global_success_check = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Global Success Check', store=True, compute='_compute_global_success_check')

    @api.depends('unit_check', 'sleeve_check', 'case_check', 'subunit_check', 'shelf_life_check', 'keep_cold_check')
    def _compute_global_success_check(self):
        for rec in self:
            if (rec.unit_check == 'ok' and rec.sleeve_check == 'ok' 
                    and rec.case_check == 'ok' and rec.subunit_check == 'ok'
                    and rec.shelf_life_check == 'ok' and rec.keep_cold_check == 'ok'):
                rec.global_success_check = 'ok'
            else:
                rec.global_success_check = 'not_ok'



    # def action_view_coding_lines(self):
    #     self.ensure_one()
    #     action = {
    #         'res_model': 'coding.log.line',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'list,form',
    #         'domain': [('coding_log_id', '=', self.id)],
    #     }
    #     return action