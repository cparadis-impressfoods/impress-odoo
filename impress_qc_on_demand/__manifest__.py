# -*- encoding: utf-8 -*-

{
    'name': 'impress_qc_on_demand',
    'version': '1.0',
    'description': 'Backport of the V18 on demand quality check feature',
    'summary': 'Quality checks on demand - Impress',
    'author': 'Cédric Paradis',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'quality','quality_control', 'stock'
    ],
    'data': [
        'views/stock_picking_views.xml',
        'wizard/on_demand_quality_check_wizard_views.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}