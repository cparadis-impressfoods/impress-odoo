# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Xray_log_line(models.Model):
    _name = 'x_ray.log.line'
    _inherit = 'log_line.mixin'
    _rec_name = "sequence"
    _description = 'X-Ray Detector Log Line'

    _sql_constraints = [
        ('unique_sequence_number', 'UNIQUE(sequence)', 'Sequence Number must be unique!'),
    ]
    
    sequence = fields.Char('Sequence', default=lambda self:_('New'), copy=False)
    
    x_ray_log_id = fields.Many2one('x_ray.log', 'X-Ray log',  compute="_compute_x_ray_log_id", store=True)
    
    reject_value = fields.Integer('Reject Value')
    
    stainless_detection_value = fields.Integer('Stainless Detection Value')
    ceramic_detection_value = fields.Integer('Ceramic Detection Value')
    glass_detection_value = fields.Integer('Glass Detection Value')

    ejection = fields.Selection([('ok', 'Ok'), ('not_ok', 'Not Ok')], 'Ejection')
    last_check_for_product = fields.Boolean('Last check for product')
    
    total_qty = fields.Integer('Total Quantity')
    reject_qty = fields.Integer('Reject Quantity')
    average = fields.Integer('Average')

    @api.depends('quality_check_id')
    def _compute_x_ray_log_id(self):
        for record in self:
            # Get the current worksheet field
            ws = record.active_worksheet_field
            if ws:
                record.x_ray_log_id = record[ws].x_x_ray_log_id
            else:
                record.x_ray_log_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sequence' not in vals or vals['sequence'] == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('x_ray_log_line') or _('New')
        return super().create(vals_list)

    def action_view_log(self):
        self.ensure_one()
        action = {
            'res_model': 'x_ray.log',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.x_ray_log_id.id,
        }
        return action