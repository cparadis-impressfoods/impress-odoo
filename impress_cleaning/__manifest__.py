# -*- encoding: utf-8 -*-
{
    'name': 'impress_cleaning',
    'version': '1.0.1',
    'description': 'Impress cleaning',
    'summary': 'Module to handle cleanings for Impress Foods',
    'author': 'Cédric Paradis',
    'website': '',
    'license': 'LGPL-3',
    'category': 'maintenance',
    'depends': [
        'maintenance',
        'mrp',
        'mrp_workorder',
        'mrp_maintenance'
    ],
    'data': [
        'actions/server_actions.xml',
        'data/maintenance_teams.xml',
        'views/maintenance_views.xml'
    ],

    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_backend': [
            'impress_cleaning/static/src/cleaning_request_button.xml',
        ]
        
    }
}