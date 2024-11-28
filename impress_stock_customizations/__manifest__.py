{
    'name': "impress_stock_customizations",
    'version': '1.0.2',
    'depends': ['base', 'stock', 'quality_control'],
    'author': "Cédric Paradis",
    'category': 'Inventory',
    'description': """
    Customizations for the stock module developped in-house by Impress Foods SEC
    """,
    # data files always loaded at installation
    'data': [
        'reports/impress_stock_customizations_stock_delivery_document_views.xml',
        'reports/impress_stock_customizations_labels.xml',
        'views/impress_stock_customizations_lot_views.xml',
        'views/online_sale_labels.xml',
        'actions/automation_rules.xml',
        'actions/server_actions.xml'
    ],
    'assets': {
        'web.assets_common': [
            'impress_stock_customizations/static/src/css/*'
        ]
    }
}