# -*- coding: utf-8 -*-
{
    'name': 'Audit_reports',
    'version': '17.0.0.0.1',
    'summary': """ Audit_reports Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Hidden',
    'depends': ['base','stock', 'product_expiry', 'mrp', 'sale_stock', 'purchase_stock'],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_lot_views.xml",
        "reports/lot_audit_report.xml"
    ],
    'assets': {
            'web.assets_backend': [
                'audit_reports/static/src/**/*',
                'audit_reports/static/src/scss/audit_report.scss',
            ],
        },
    
    'installable': True,
    'auto_install': False,
    'license': 'GPL-2',
}
