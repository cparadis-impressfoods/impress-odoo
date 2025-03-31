# -*- coding: utf-8 -*-
import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    qty_per_pallet = fields.Float(string="Quantity per Pallet")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_per_pallet = fields.Float(
        string="Quantity per Pallet",
        compute="_compute_qty_per_pallet",
        inverse="_set_qty_per_pallet",
    )

    def _compute_qty_per_pallet(self):
        self._compute_template_field_from_variant_field("qty_per_pallet")

    def _set_qty_per_pallet(self):
        self._set_product_variant_field("qty_per_pallet")
