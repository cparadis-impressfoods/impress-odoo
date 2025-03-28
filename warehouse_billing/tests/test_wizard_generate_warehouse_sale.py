# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.tests import TransactionCase,tagged

@tagged('standard', 'warehouse_billing')
class TestGenerateWarehouseSaleOrder(TransactionCase):

    def setUp(self):
        super(TestGenerateWarehouseSaleOrder, self).setUp()
        self.current_date = datetime.strptime('2025-03-31', '%Y-%m-%d')
        self.wizard = self.env['wizard.generate.warehouse.sale.order']
        
        self.billing_product = self.env['product.product'].create({
            'name': 'Billing Product',
            'type': 'service',
            'detailed_type': 'service',
        })

        self.partner_1 = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TEST',
        })

        self.config = self.env['warehouse.billing.config'].create({
            'name': 'Test Config',
            'partner_id': self.partner_1.id,
            'warehouse_id': self.warehouse.id,
            'rate': 10.0,
            'billing_product_id': self.billing_product.id
        })
    
    def test_end_of_month_31_day_month_31(self):
        test_date = datetime.strptime('2025-03-31', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertTrue(is_end_of_month, f"{test_date}")
    
    def test_end_of_month_31_day_month_30(self):

        test_date = datetime.strptime('2025-03-30', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertFalse(is_end_of_month, f"{test_date}")

    def test_end_of_month_30_day_month_30(self):
        test_date = datetime.strptime('2025-04-30', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertTrue(is_end_of_month, f"{test_date}")
    
    def test_end_of_month_30_day_month_29(self):

        test_date = datetime.strptime('2025-04-29', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertFalse(is_end_of_month, f"{test_date}")
    
    def test_end_of_month_28_day_month_28(self):
        test_date = datetime.strptime('2025-02-28', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertTrue(is_end_of_month, f"{test_date}")

    def test_end_of_month_28_day_month_27(self):
        test_date = datetime.strptime('2025-02-27', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertFalse(is_end_of_month, f"{test_date}")

    def test_end_of_month_29_day_month_29(self):
        test_date = datetime.strptime('2028-02-29', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertTrue(is_end_of_month, f"{test_date}")

    def test_end_of_month_29_day_month_28(self):
        test_date = datetime.strptime('2028-02-28', '%Y-%m-%d')
        is_end_of_month = self.wizard.end_of_month(test_date)
        self.assertFalse(is_end_of_month, f"{test_date}")

    def test_group_by_partner_1_partner(self):        
        configs = self.env['warehouse.billing.config'].create([
            {'name': 'Config 1', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},
            {'name': 'Config 2', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},
        ])

        grouped_configs = self.wizard.group_by_partner(configs)
        self.assertEqual(len(grouped_configs), 1, "All configs should be grouped into one partner")
        
    def test_group_by_partner_2_partners(self):
        configs = self.env['warehouse.billing.config'].create([
            {'name': 'Config 1', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},
            {'name': 'Config 2', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},
            {'name': 'Config 3', 'partner_id': self.partner_2.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},
            {'name': 'Config 4', 'partner_id': self.partner_2.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id},

        ])
        grouped_configs = self.wizard.group_by_partner(configs)
        self.assertEqual(len(grouped_configs), 2, "All configs should be grouped into 2 partners")

    def test_get_configs_to_bill(self):
        config_model = self.env['warehouse.billing.config']
        configs_to_bill = config_model.create([
            {'name': 'Config Monthly Last Day of Month', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'monthly', 'bill_last_day_month': True, 'last_invoice_date': datetime.strptime('2025-02-28', '%Y-%m-%d')},
            {'name': 'Config Monthly Specific Day', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'monthly', 'billing_day_month': 22, 'last_invoice_date': datetime.strptime('2025-02-22', '%Y-%m-%d')},
            {'name': 'Config Weekly', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'weekly', 'billing_day_week': 1, 'last_invoice_date': datetime.strptime('2025-03-17', '%Y-%m-%d')},
            {'name': 'Config Weekly late', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'weekly', 'billing_day_week': 1, 'last_invoice_date': datetime.strptime('2025-03-10', '%Y-%m-%d')},
            {'name': 'Config Daily', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'daily', 'last_invoice_date': datetime.strptime('2025-03-12', '%Y-%m-%d')},
        ])

        configs_not_to_bill = config_model.create([            
            {'name': 'Config Monthly early', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'monthly', 'billing_day_month': 12, 'last_invoice_date': datetime.strptime('2025-03-12', '%Y-%m-%d')},
            {'name': 'Config Weekly early', 'partner_id': self.partner_1.id, 'warehouse_id': self.warehouse.id, 'rate': 10.0, 'billing_product_id': self.billing_product.id,
                'billing_cycle': 'weekly', 'billing_day_week': 7, 'last_invoice_date': datetime.strptime('2025-03-30', '%Y-%m-%d')},
        ])

        check_date = datetime.strptime('2025-03-31', '%Y-%m-%d')
        configs = self.wizard.get_configs_to_bill(check_date)
        configs = configs.filtered_domain([('partner_id', '=', self.partner_1.id)])
        self.assertEqual(len(configs), len(configs_to_bill), f"{len(configs_to_bill)} configs should be returned. {[config.name for config in configs]}")
        