# -*- coding: utf-8 -*-
{
    'name': 'Impress Quality Logs',
    'version': '17.0.0.1.0',
    'summary': """ Implements many quality logs used by Impress Foods for quality control """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Manufacturing',
    'depends': ['base', 'web', 'stock', 'mrp', 'quality_control', 
                'quality_mrp', 'mrp_workorder', 'sign', 'quality_mrp_workorder_worksheet'],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "data/actions.xml",
        "views/hpp_log_views.xml",
        "views/hpp_log_line_views.xml",
        "views/loma_log_views.xml",
        "views/loma_log_line_views.xml",
        "views/metal_log_views.xml",
        "views/metal_log_line_views.xml",
        "views/coding_log_views.xml",
        "views/product_product_views.xml",
        "views/mrp_production_views.xml",
        "views/menus.xml",
        
    ],
    'assets': {
              #'web.assets_backend': [
              #    'impress_quality_logs/static/src/**/*'
              #],
          },

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'GPL-2',
}
