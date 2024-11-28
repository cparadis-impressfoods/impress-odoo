# -*- encoding: utf-8 -*-

{
    'name': 'impress_qc_on_demand_mrp',
    'version': '1.0',
    'description': 'Backport of the V18 on demand quality check feature',
    'summary': 'Quality checks on demand - Impress',
    'author': 'Cédric Paradis',
    'website': '',
    'license': 'GPL-2',
    'category': '',
    'depends': [
        'quality','quality_control', 'mrp', 'mrp_workorder', 'quality_mrp', 'impress_qc_on_demand'
    ],
    'data': [
        'views/mrp_production_views.xml',
        'wizard/on_demand_quality_check_wizard_views.xml',
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}