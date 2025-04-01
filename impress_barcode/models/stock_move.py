# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_fields_stock_barcode(self):
        return [
            "id",
            "name",
            "picking_id",
            "product_id",
            "lot_ids",
            "product_qty",
            "quantity",
            "product_uom_qty",
        ]
