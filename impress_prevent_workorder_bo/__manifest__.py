# -*- coding: utf-8 -*-
{
    'name': 'Impress_prevent_workorder_bo',
    'version': '0.1.0',
    'summary': """ Prevent BO on on Workorders""",
    'description': """ Prevents the creation of BO on workorder validation when producing less than expected.""",
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Hidden',
    'depends': ['base', 'mrp_workorder' ],
    'data': [
        
    ],
    'assets': {
            'web.assets_backend': [
                'impress_prevent_workorder_bo/static/src/**/*.js'
            ],
        },
    'installable': True,
    'license': 'GPL-2',
}
