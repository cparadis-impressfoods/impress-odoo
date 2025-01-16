# -*- coding: utf-8 -*-
{
    'name': "impress_barcode",

    'summary': "Customizations to barcode app",

    'description': """
        Customizations to barcode app
    """,

    'author': "Cédric Paradis",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '0.1.0',
    'license': 'GPL-2',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale_management', 'stock_barcode'],

    # always loaded
    'data': [
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend':[
            "impress_barcode/static/src/components/move.xml",
            "impress_barcode/static/src/components/move.js",
            "impress_barcode/static/src/components/line.xml",
            "impress_barcode/static/src/components/main.js",
            "impress_barcode/static/src/components/main.xml",
            "impress_barcode/static/src/main.xml",
            "impress_barcode/static/src/**/*.js",
        ],
        'web.assets_common': [
            "impress_barcode/static/src/**/*.css",
        ]


    }

}

