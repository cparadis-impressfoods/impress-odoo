# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MetalLogLine(models.Model):
    _name = 'metal.log.line'
    _inherit = 'log_line.mixin'
    _description = 'Metal_log_line'
    _rec_name = 'sequence'

    _sql_constraints = [
        ('unique_sequence_number', 'UNIQUE(sequence)', 'Sequence Number must be unique!'),
    ]

    metal_log_id = fields.Many2one(comodel_name='metal.log', compute="_compute_metal_log_id", store=True)

    sequence = fields.Char('Sequence', default=lambda self: _('New'), copy=False)

    calibration = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Calibration')
    ejection = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Ejection')
    
    reject_value = fields.Float('Reject Value')
    ferrous = fields.Integer('Ferrous')
    non_ferrous = fields.Integer('Non Ferrous')
    stainless = fields.Integer('Stainless')
    torque = fields.Integer('Torque')
    mean_weight = fields.Float('Mean Weight')
    

    @api.depends('quality_check_id')
    def _compute_metal_log_id(self):
        for record in self:
            # Get the current worksheet field
            ws = record.active_worksheet_field
            if ws:
                record.metal_log_id = record[ws].x_metal_log_id
            else:
                record.metal_log_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sequence' not in vals or vals['sequence'] == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('metal_log_line') or _('New')
        return super().create(vals_list)

    def action_view_log(self):
        self.ensure_one()
        action = {
            'res_model': 'metal.log',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.metal_log_id.id,
        }
        return action