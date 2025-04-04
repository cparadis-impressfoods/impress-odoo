# -*- coding: utf-8 -*-
import logging

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError

_logger_ = logging.getLogger(__name__)


@tagged("standard", "impress")
class TestMaintenanceRequest(TransactionCase):
    def setUp(self):
        super(TestMaintenanceRequest, self).setUp()
        self.request_model = self.env["maintenance.request"]

        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
            }
        )

        self.scrap = self.env["stock.scrap"]

    def test_create_scrap(self):
        request = self.request_model.create(
            {
                "name": "Test Request",
            }
        )

        self.scrap.create(
            {
                "maintenance_request_id": request.id,
                "product_id": self.product.id,
                "scrap_qty": 10,
            }
        )

        self.assertEqual(len(request.scrap_ids), 1)

    def test_delete_draft_scrap(self):
        request = self.request_model.create(
            {
                "name": "Test Request",
            }
        )
        scrap_move = self.scrap.create(
            {
                "maintenance_request_id": request.id,
                "product_id": self.product.id,
                "scrap_qty": 10,
            }
        )
        scrap_move.unlink()
        self.assertEqual(len(request.scrap_ids), 0)

    def test_delete_done_scrap(self):
        request = self.request_model.create(
            {
                "name": "Test Request",
            }
        )
        scrap_move = self.scrap.create(
            {
                "maintenance_request_id": request.id,
                "product_id": self.product.id,
                "scrap_qty": 10,
            }
        )
        scrap_move.do_scrap()
        self.assertRaises(UserError, scrap_move.unlink)

    def test_delete_request_with_draft_scrap(self):
        request = self.request_model.create(
            {
                "name": "Test Request",
            }
        )
        self.scrap.create(
            {
                "maintenance_request_id": request.id,
                "product_id": self.product.id,
                "scrap_qty": 10,
            }
        )

        qty_before = len(
            self.env["stock.scrap"].search([("product_id", "=", self.product.id)])
        )

        request.unlink()
        qty_after = len(
            self.env["stock.scrap"].search([("product_id", "=", self.product.id)])
        )
        self.assertEqual(1, qty_before)
        self.assertEqual(0, qty_after)

    def test_delete_request_with_done_scrap(self):
        request = self.request_model.create(
            {
                "name": "Test Request",
            }
        )
        scrap_move = self.scrap.create(
            {
                "maintenance_request_id": request.id,
                "product_id": self.product.id,
                "scrap_qty": 10,
            }
        )
        scrap_move.do_scrap()
        self.assertRaises(UserError, request.unlink)
