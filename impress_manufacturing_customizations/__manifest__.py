{
    'name': "impress_manufacturing_customizations",
    'version': '0.1.1',
    'depends': ['base', 'mrp'],
    'author': "Cédric Paradis",
    'category': 'Manufacturing',
    'description': """"
    Customizations for the manufacturing module
    """,
    'license': 'GPL-2',
    # data files always loaded at installation
    "data": [
        "views/impress_mrp_customizations_production_order_views.xml",
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
}