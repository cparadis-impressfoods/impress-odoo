# -*- coding: utf-8 -*-
{
    'name': 'impress_deposit',
    'version': '17.0.0.1',
    'summary': """ Impress_deposit Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Stock',
    'depends': ['base', 'web', 'sale_management', 'stock'],
    
    "data": [
        "views/product_product_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
        "views/stock_picking_views.xml"
    ],
    
    'assets': {
              #'web.assets_backend': [
              #    'impress_deposit/static/src/**/*'
              #],
          },

    'installable': True,
    'auto_install': False,
    'license': 'GPL-2',
}
