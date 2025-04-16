from datetime import datetime
from math import ceil

from odoo.tests import TransactionCase, tagged


@tagged("standard", "impress")
class TestWarehouseBillingConfig(TransactionCase):
    def setUp(self):
        super().setUp()
        self.billing_config = self.env["warehouse.billing.config"]
        self.date = datetime.strptime("2025-03-31", "%Y-%m-%d").date()

        self.billing_product = self.env["product.product"].create(
            {
                "name": "Billing Product",
                "type": "service",
                "detailed_type": "service",
                "taxes_id": False,
            }
        )

        self.product_1 = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "detailed_type": "product",
                "qty_per_pallet": 10,
                "taxes_id": False,
            }
        )

        self.product_2 = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "detailed_type": "product",
                "qty_per_pallet": 100,
                "taxes_id": False,
            }
        )

        self.partner_1 = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        self.partner_2 = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        self.warehouse = self.env["stock.warehouse"].create(
            {
                "name": "Test Warehouse",
                "code": "TEST",
            }
        )

        self.config_1 = self.env["warehouse.billing.config"].create(
            {
                "name": "Test Config",
                "partner_id": self.partner_1.id,
                "warehouse_id": self.warehouse.id,
                "rate": 10.0,
                "base_qty": 10.0,
                "billing_product_id": self.billing_product.id,
                "billing_cycle": "daily",
                "last_invoice_date": datetime.strptime("2025-03-30", "%Y-%m-%d"),
                "filter_domain": f"[('product_id', '=', {self.product_1.id})]",
            }
        )

        self.config_2 = self.env["warehouse.billing.config"].create(
            {
                "name": "Test Config",
                "partner_id": self.partner_2.id,
                "warehouse_id": self.warehouse.id,
                "rate": 10.0,
                "base_qty": 10,
                "flat_fee": 150,
                "billing_product_id": self.billing_product.id,
                "billing_cycle": "daily",
                "last_invoice_date": datetime.strptime("2025-03-30", "%Y-%m-%d"),
                "filter_domain": f"[('product_id', '=', {self.product_2.id})]",
            }
        )

    def test_single_billing_config_pallets(self):
        quant_history = self.env["warehouse.quant.history"].create(
            {
                "product_id": self.product_1.id,
                "quantity": 10,
                "location_id": self.warehouse.lot_stock_id.id,
                "warehouse_id": self.warehouse.id,
                "date": datetime.strptime("2025-03-31", "%Y-%m-%d"),
            }
        )

        # We should have a single sale order with a single sale order line
        sale_order = self.billing_config.with_context(
            warehouse_billing_date=self.date
        ).bill_config(self.config_1)

        qty_in_pallets = ceil(quant_history.quantity / self.product_1.qty_per_pallet)
        total_usage = qty_in_pallets + self.config_1.base_qty
        total_amount = total_usage * self.config_1.rate + self.config_1.flat_fee

        quant_group = self.env["warehouse.quant.group"].search(
            [("sale_order_id", "=", sale_order.id)]
        )

        n_sale_order_line = len(sale_order.order_line)
        n_quant_group = len(quant_group)
        n_quant_history = len(quant_group.quant_history_ids)

        self.assertEqual(
            n_sale_order_line, 1, f"Expected 1 sale order line, got {n_sale_order_line}"
        )
        self.assertEqual(
            n_quant_group, 1, f"Expected 1 quant group, got {n_quant_group}"
        )
        self.assertEqual(
            n_quant_history,
            1,
            f"Expected 1 quant_history in the usage group, got {n_quant_history}",
        )
        self.assertEqual(
            sale_order.order_line.product_id,
            self.billing_product,
            "Wrong product added to the sale order line",
        )
        self.assertEqual(
            sale_order.amount_total,
            total_amount,
            f"Expected total amount to be {total_amount}, got {sale_order.amount_total}",
        )
        self.assertEqual(
            sale_order.partner_id,
            self.config_1.partner_id,
            "Expected the partner id to be the same as the config",
        )

    def test_multiple_billing_config_pallets(self):
        quant_history_1 = self.env["warehouse.quant.history"].create(
            {
                "product_id": self.product_1.id,
                "quantity": 10,
                "location_id": self.warehouse.lot_stock_id.id,
                "warehouse_id": self.warehouse.id,
                "date": datetime.strptime("2025-03-31", "%Y-%m-%d"),
            }
        )
        quant_history_2 = self.env["warehouse.quant.history"].create(
            {
                "product_id": self.product_2.id,
                "quantity": 100,
                "location_id": self.warehouse.lot_stock_id.id,
                "warehouse_id": self.warehouse.id,
                "date": datetime.strptime("2025-03-31", "%Y-%m-%d"),
            }
        )

        # We should have a single sale order with a single sale order line
        sale_order = self.billing_config.with_context(
            warehouse_billing_date=self.date
        ).bill_config(self.config_1 + self.config_2)
        sale_order_lines = sale_order.order_line
        quant_group = self.env["warehouse.quant.group"].search(
            [("sale_order_id", "=", sale_order.id)]
        )

        n_quant_group = len(quant_group)
        n_quant_history = len(quant_group.quant_history_ids)
        n_sale_order = len(sale_order)
        n_sale_order_line = len(sale_order.order_line)

        self.assertEqual(
            len(sale_order), 1, f"Expected 1 sale order, got {n_sale_order}"
        )
        self.assertEqual(
            n_sale_order_line, 2, f"Expected 2 sale order line, got {n_sale_order_line}"
        )
        self.assertEqual(
            n_quant_group, 2, f"Expected 2 quant group, got {n_quant_group}"
        )
        self.assertEqual(
            n_quant_history,
            2,
            f"Expected 2 quant_history in the usage group, got {n_quant_history}",
        )
        self.assertEqual(
            sale_order.partner_id,
            self.config_1.partner_id,
            "Expected the partner id to be the same as the config",
        )

        quants = [quant_history_1, quant_history_2]
        configs = [self.config_1, self.config_2]

        for i in range(2):
            quant_history = quants[i]
            order_line = sale_order_lines[i]
            config = configs[i]

            qty_in_pallets = ceil(
                quant_history.quantity / quant_history.product_id.qty_per_pallet
            )
            total_usage = qty_in_pallets + config.base_qty
            total_amount = total_usage * config.rate + config.flat_fee

            self.assertEqual(
                order_line.product_id,
                self.billing_product,
                "Wrong product added to the sale order line",
            )
            self.assertEqual(
                order_line.price_subtotal,
                total_amount,
                f"Expected total amount to be {total_amount}, got {order_line.price_subtotal}",
            )
