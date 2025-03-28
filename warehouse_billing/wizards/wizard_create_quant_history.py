# -*- coding: utf-8 -*-
import logging
import typing
from datetime import datetime, timedelta
from typing import Any
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class WizardCreate_quant_history(models.TransientModel):
    _name = 'wizard.create_quant_history'
    _description = _('WizardCreate_quant_history')

    name = fields.Char(_('Name'))

    product_id = fields.Many2one('product.product', domain=[('type', '=', 'product')])
    tracking = fields.Selection(related="product_id.tracking")
    uom_id = fields.Many2one("uom.uom")
    quantity = fields.Float()
    lot_id = fields.Many2one('stock.lot', domain=[('product_id' '=', lambda self: self.product_id)])
    warehouse_id = fields.Many2one('stock.warehouse')
    location_id = fields.Many2one('stock.location', domain=[('usage', '=', 'internal')])
    date_from = fields.Date()
    date_to = fields.Date(default=fields.Date.context_today)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            record.uom_id = record.product_id.uom_id

    def create_quant_history(self):
        if not self.product_id or not self.location_id or not self.warehouse_id:
            raise UserError("Missing fields!")

        quant_history = self.env['warehouse.quant.history']
        current_date = self.date_from
        values:list[dict[str, Any]] = []
        
        while current_date <= self.date_to:
            values.append({
                'date': current_date,
                'product_id': self.product_id.id,
                'quantity': self.quantity,
                'lot_id': self.lot_id.id,
                'location_id': self.location_id.id,
                'warehouse_id': self.warehouse_id.id
            })
            current_date += timedelta(days=1)
        
        quants = quant_history.create(values)
        return quants   