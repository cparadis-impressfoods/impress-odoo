# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = "mrp.production"

    def _prepare_stock_lot_values(self):
        self = self.with_context(julian_product_id=self.product_id.id)  # type: ignore
        res = super(MrpProduction, self)._prepare_stock_lot_values()
        return res
