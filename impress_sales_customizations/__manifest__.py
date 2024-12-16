{
    'name': "impress_sales_customizations",
    'version': '0.1.0',
    'depends': ['base', 'sale_management'],
    'author': "Cédric Paradis",
    'category': 'Sales',
    'description': """"
    Customizations for the sales module
    """,
    'license': 'GPL-2',
    # data files always loaded at installation
    'data': [
        'views/impress_sales_customizations_sales_order_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
}