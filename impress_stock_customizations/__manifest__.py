{
    'name': "impress_stock_customizations",
    'version': '0.1.0',
    'depends': ['base', 'stock', 'quality_control'],
    'author': "Cédric Paradis",
    'category': 'Inventory',
    'description': """
    Customizations for the stock module developped in-house by Impress Foods SEC
    """,
    'license': 'GPL-2',
    # data files always loaded at installation
    'data': [
        'reports/impress_stock_customizations_stock_delivery_document_views.xml',
        'reports/impress_stock_customizations_labels.xml',
        'views/impress_stock_customizations_lot_views.xml',
        'reports/online_sale_labels.xml',
    ],
    'assets': {
        'web.assets_common': [
            'impress_stock_customizations/static/src/css/*'
        ]
    }
}