# -*- coding: utf-8 -*-
{
    'name': 'impress_production_billing',
    'version': '17.0.1.0.1',
    'summary': """ Module to allow billing of MOs directly through SOs """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Sales',
    'depends': ['base', 'web', 'mrp', 'purchase', 'sale_management'],
    'data': [
        'views/mrp_production_views.xml'
    ],
    'installable': True,
    'license': 'GPL-2',
}
