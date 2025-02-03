# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one('product.product', 'Product used for deposit',
                                         ondelete='cascade', required=False,
                                         config_parameter="impress_deposit.deposit_product",
                                         domain=[('detailed_type', '=', 'service')] )

