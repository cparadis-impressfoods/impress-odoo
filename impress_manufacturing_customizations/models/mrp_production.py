# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sequence = fields.Integer('Sequence')
    product_category_id = fields.Many2one('product.category', 'Product Category', 
                                            related="product_tmpl_id.categ_id", store=True, depends=["product_tmpl_id"])