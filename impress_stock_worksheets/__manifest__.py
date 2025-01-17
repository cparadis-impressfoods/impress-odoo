# -*- coding: utf-8 -*-
{
    'name': 'impress_stock_worksheets',
    # Non semantic version to allow to tag the most recent document date
    'version': '25.01.14',
    'summary': """ Impress_stock_worksheets Summary """,
    'author': 'Cédric Paradis',
    'category': 'Hidden',
    'depends': ['base', 'stock', 'worksheet', 'quality_control_worksheet'],
    'data': [
        # Fichiers en date du 2025-01-14
        'data/receipt/ReceiptWorksheet_20250114.xml',
        'views/receipt/ReceiptWorksheet_20250114.xml',
        'reports/receipt/ReceiptWorksheet_20250114.xml',
        'data/delivery/DeliveryWorksheet_20250114.xml',
        'views/delivery/DeliveryWorksheet_20250114.xml'
        
    ],

    'installable': True,
    'auto_install': False,
    'license': 'GPL-2',
}
