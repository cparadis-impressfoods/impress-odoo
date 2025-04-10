# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    billing_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Billing Product",
        domain=[("type", "=", "service")],
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    billing_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Billing Product",
        domain=[("type", "=", "service")],
        compute="_compute_billing_product",
        inverse="_set_billing_product",
    )

    def _compute_billing_product(self):
        self._compute_template_field_from_variant_field("billing_product_id")

    def _set_billing_product(self):
        self._set_product_variant_field("billing_product_id")
