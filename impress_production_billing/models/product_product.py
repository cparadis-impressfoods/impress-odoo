import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    billing_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Billing Product",
        domain=[("type", "=", "service")],
    )

    def get_production_billing_product(self):
        self.ensure_one()
        if self.billing_product_id:
            return self.billing_product_id

        reference_to_match = "S" + self.default_code[1:]
        matching_product = self.env["product.product"].search(
            [("default_code", "=", reference_to_match)]
        )
        if matching_product:
            return matching_product
        else:
            raise ValidationError(
                _(
                    "No matching service product found."
                    f"Expected product with reference {reference_to_match}"
                )
            )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    billing_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Billing Product",
        domain=[("type", "=", "service")],
        compute="_compute_billing_product",
        inverse="_inverse_billing_product",
    )

    def _compute_billing_product(self):
        self._compute_template_field_from_variant_field("billing_product_id")

    def _inverse_billing_product(self):
        self._set_product_variant_field("billing_product_id")
