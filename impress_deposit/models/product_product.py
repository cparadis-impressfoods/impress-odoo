# -*- coding: utf-8 -*-
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    requires_deposit = fields.Boolean("Requires Deposit")
    qty_multiple = fields.Integer("Quantity for deposit")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_deposit = fields.Boolean(
        "Requires Deposit",
        compute="_compute_requires_deposit",
        inverse="_set_requires_deposit",
    )
    qty_multiple = fields.Integer(
        "Quantity for deposit",
        compute="_compute_qty_multiple",
        inverse="_set_qty_multiple",
    )

    def _compute_requires_deposit(self):
        self._compute_template_field_from_variant_field("requires_deposit")

    def _set_requires_deposit(self):
        self._set_product_variant_field("requires_deposit")

    def _compute_qty_multiple(self):
        self._compute_template_field_from_variant_field("qty_multiple")

    def _set_qty_multiple(self):
        self._set_product_variant_field("qty_multiple")
