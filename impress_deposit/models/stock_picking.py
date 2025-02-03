# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    container_qty = fields.Integer('Number of containers shipped', compute='_compute_container_qty')

    @api.depends('move_line_ids', 'move_line_ids.state')
    def _compute_container_qty(self):
        for record in self:
            total = 0
            
            for line in record.move_line_ids:
                total += line.container_qty

            record.container_qty = total
