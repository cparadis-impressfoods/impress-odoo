# -*- coding: utf-8 -*-

{
    'name': "Impress Account report customizations",
    'version': '0.1.0',
    'depends': ['account_accountant'],
    'author': "Cédric Paradis",
    'category': 'Accounting',
    'description': """
    Module to customize the accounting reports 
    """,
    
    # data files always loaded at installation
    'assets': {
        'web.assets_backend':[
            'impress_account_report/static/src/account_report.xml',
        ],
    },

    'license': 'GPL-2',
    'installable': True,
}