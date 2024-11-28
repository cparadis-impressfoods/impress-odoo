{
    'name': "impress_test_shop_floor",
    'version': '1.0.3',
    'depends': ['mrp_workorder'],
    'author': "Cédric Paradis",
    'category': 'Manufacturing',
    'description': """
    Test for shop floor customizations by mean of data module
    """,
    # data files always loaded at installation
    'data': [
    ],
    'license': 'GPL-2',
    'assets': {
        'web.assets_backend': [
            'TestPatchingShopFloor/static/src/**/*.xml',
            'TestPatchingShopFloor/static/src/**/*.js'
        ],
    }
}