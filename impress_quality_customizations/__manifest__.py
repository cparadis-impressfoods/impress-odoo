{
    'name': "impress_quality_customizations",
    'version': '1.0.0',
    'depends': ['base', 'quality_control'],
    'author': "Cédric Paradis",
    'category': 'Quality',
    'description': """
    Customizations for the quality module developped in-house by Impress Foods SEC
    """,
    # data files always loaded at installation
    'data': [
        'views/impress_quality_customizations_quality_check_views.xml',
        'views/impress_quality_customizations_menus.xml'
    ],
    'assets': {
    }
}