# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    requires_deposit = fields.Boolean(related='product_id.requires_deposit', depends=['product_id'])
    container_qty = fields.Integer('Container Quantity', compute='_compute_container_qty')




    @api.depends('state')
    def _compute_container_qty(self):
        for record in self:
            if record.state == 'done' and record.requires_deposit:
                record.container_qty = record.quantity * record.product_id.qty_multiple
            else:
                record.container_qty = 0
