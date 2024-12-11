# -*- coding: utf-8 -*-
{
    'name': 'Documents_archive',
    'version': '0.0.1',
    'summary': """ Documents_archive Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Hidden',
    'depends': ['base', 'documents', 'stock'],
    "data": [
        "views/documents_document_views.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'documents_archive/static/src/**/*.js',
            'documents_archive/static/src/**/*.xml',
            'documents_archive/static/src/**/*.scss',
        ]
    },

    'installable': True,
    'license': 'GPL-2',
}