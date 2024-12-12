# -*- coding: utf-8 -*-
{
    'name': 'Shop_floor_show_manual_qc',
    'version': '0.0.1',
    'summary': """ Shop_floor_show_manual_qc Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Hidden',
    'depends': ['base', 'mrp_workorder' , 'quality_control', 'stock', 'impress_qc_on_demand_mrp'],
    'data': [
        
    ],
    'assets': {
        'web.assets_backend': [
            'shop_floor_show_manual_qc/static/src/**/*.js',
            'shop_floor_show_manual_qc/static/src/**/*.xml',
            'shop_floor_show_manual_qc/static/src/**/*.scss',
        ]
    },

    'installable': True,

    'license': 'GPL-2',
}
