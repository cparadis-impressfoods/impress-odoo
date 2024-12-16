# -*- coding: utf-8 -*-
{
    'name': 'impress_purchase_customizations',
    'version': '0.1.0',
    'summary': 'Impress Foods purchase customizations',
    'description': """
        Impress Foods purchase customizations
    """,
    'category': 'Accounting/Manufacturing',
    'author': 'Cédric Paradis',
    'license': 'GPL-2',
    
    # Dependencies
    'depends': [
        'base',
        'account',
        'purchase',
        'product',
        'analytic',
    ],
    
    # Data files always loaded
    'data': [
        'actions/impress_purchase_customizations_actions.xml',

    ],
    
    # Technical configuration
    'sequence': 100,
}