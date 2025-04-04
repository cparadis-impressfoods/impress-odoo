# -*- coding: utf-8 -*-
{
    "name": "Maintenance - Documents",
    "version": "17.0.1.0.0",
    "summary": """ Bridge module between Maintenance and Documents """,
    "description": """ Allows documents to be assigned to maintenance equipments """,
    "author": "Cédric Paradis",
    "website": "",
    "category": "Hidden",
    "depends": [
        "base",
        "documents",
        "maintenance_worksheet",
    ],
    "data": [
        "views/maintenance_equipment_views.xml",
        "data/document_folder.xml",
    ],
    "installable": True,
    "auto_install": True,
    "license": "GPL-2",
}
