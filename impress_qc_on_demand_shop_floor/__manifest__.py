# -*- encoding: utf-8 -*-

{
    'name': 'impress_qc_on_demand_shop_floor',
    'version': '0.1.0',
    'description': 'Backport of the V18 on demand quality check feature - adding UI to shop floor app',
    'summary': 'Quality checks on demand - Impress',
    'author': 'Cédric Paradis',
    'website': '',
    'license': 'GPL-2',
    'category': '',
    'depends': [
         'impress_qc_on_demand', 'mrp_workorder', 'impress_qc_on_demand_mrp'
    ],
    'data': [

    ],
    'auto_install': ['impress_qc_on_demand_mrp', 'mrp_workorder', 'impress_qc_on_demand'],

    'assets': {
        "web.assets_backend": [
            'impress_qc_on_demand_shop_floor/static/src/**/*',
        ]
    }
}