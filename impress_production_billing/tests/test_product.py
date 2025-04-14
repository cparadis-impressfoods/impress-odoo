# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase, tagged


@tagged("standard", "impress")
class TestProductProduct(TransactionCase):
    def setUp(self):
        super(TestProductProduct, self).setUp()

        self.product_model = self.env["product.product"]

        self.billing_product = self.product_model.create(
            {"name": "Billing Product", "type": "service", "default_code": "SPP1"}
        )

        self.product_with_billing_product = self.product_model.create(
            {
                "name": "Billing Product",
                "type": "product",
                "billing_product_id": self.billing_product.id,
            }
        )
        self.product_without_billing_product = self.product_model.create(
            {"name": "Billing Product", "type": "product", "default_code": "EPP1"}
        )

    def test_get_billing_product_billing_product_id_field(self):
        self.assertEqual(
            self.product_with_billing_product.get_production_billing_product(),
            self.billing_product,
        )

    def test_get_billing_product_reference_matching(self):
        self.assertEqual(
            self.product_without_billing_product.get_production_billing_product(),
            self.billing_product,
        )
