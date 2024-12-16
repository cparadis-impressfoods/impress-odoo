# -*- coding: utf-8 -*-
{
    'name': 'Documents_archive',
    'version': '0.1.0',
    'summary': """ Module to allow a "soft" archive feature for documents. """,
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
