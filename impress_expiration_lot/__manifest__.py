{
    'name': "impress_expiration_lot",
    'version': '1.0.0',
    'depends': ['base', 'stock', 'product_expiry', 'base_automation'],
    'author': "Cédric Paradis",
    'category': 'Inventory',
    'description': """
    Module that allows to automatically calculate to correct dates for a lot's expiry,
    """,
    # data files always loaded at installation
    'data': [
        'actions/server_actions.xml',
        'actions/automation_rules.xml'
        
    ],
    'assets': {
    }
}