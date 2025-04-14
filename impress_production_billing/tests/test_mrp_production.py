# -*- coding: utf-8 -*-
from datetime import datetime

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError


@tagged("standard", "impress")
class TestMrpProduction(TransactionCase):

    def setUp(self):
        super(TestMrpProduction, self).setUp()

        self.product_model = self.env["product.product"]
        self.mo_model = self.env["mrp.production"]
        self.so_model = self.env["sale.order"]
        self.so_line_model = self.env["sale.order.line"]

        self.partner = self.env["res.partner"].create({"name": "test partner"})

        self.billing_product = self.product_model.create(
            {"name": "Billing Product", "type": "service"}
        )

        self.product = self.product_model.create(
            {
                "name": "Test Product",
                "type": "product",
                "billing_product_id": self.billing_product.id,
            }
        )

    def test_link_mo_to_so_all_correct(self):
        reference = hash(datetime.now().strftime("%Y%m%d%H%M%S"))
        so = self.so_model.create(
            {"partner_id": self.partner.id, "client_order_ref": reference}
        )
        so_line = self.so_line_model.create(
            {
                "order_id": so.id,
                "product_id": self.billing_product.id,
                "product_uom_qty": 1,
            }
        )

        mo = self.mo_model.create(
            {
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "billing_sale_order_ref": reference,
            }
        )

        self.assertEqual(mo.billing_sale_order_id, so)
        self.assertEqual(mo.billing_sale_order_line_id, so_line)

    def test_link_mo_to_so_wrong_product(self):
        reference = hash(datetime.now().strftime("%Y%m%d%H%M%S"))
        so = self.so_model.create(
            {"partner_id": self.partner.id, "client_order_ref": reference}
        )
        self.so_line_model.create(
            {
                "order_id": so.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
            }
        )

        self.assertRaises(
            ValidationError,
            self.mo_model.create,
            {
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "billing_sale_order_ref": reference,
            },
        )

    def test_link_mo_to_so_no_line(self):
        reference = hash(datetime.now().strftime("%Y%m%d%H%M%S"))
        self.so_model.create(
            {"partner_id": self.partner.id, "client_order_ref": reference}
        )

        self.assertRaises(
            ValidationError,
            self.mo_model.create,
            {
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "billing_sale_order_ref": reference,
            },
        )

    def test_link_mo_to_so_wrong_reference(self):
        reference = hash(datetime.now().strftime("%Y%m%d%H%M%S"))
        self.so_model.create(
            {"partner_id": self.partner.id, "client_order_ref": reference}
        )

        self.assertRaises(
            ValidationError,
            self.mo_model.create,
            {
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "billing_sale_order_ref": "WRONG_REF",
            },
        )
