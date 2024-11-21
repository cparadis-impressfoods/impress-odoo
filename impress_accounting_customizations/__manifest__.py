{
    'name': "impress_accounting_customizations",
    'version': '1.0',
    'depends': ['base', 'account_accountant'],
    'author': "Cédric Paradis",
    'category': 'Accounting',
    'description': """
    Customizations for the accounting module
    """,
    # data files always loaded at installation
    'data': [
        'views/impress_accounting_customizations_account_move_views.xml',
        'actions/impress_accounting_actions.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
}