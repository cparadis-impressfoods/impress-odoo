# -*- coding: utf-8 -*-
{
    "name": "maintenance_consume_stock",
    "version": "17.0.0.0.2",
    "summary": """ Module to allow stock usage in maintenance requests """,
    "author": "Cédric Paradis",
    "website": "",
    "category": "Hidden",
    "depends": ["base", "maintenance_worksheet", "stock"],
    "data": [
        "data/locations.xml",
        "views/maintenance_request_views.xml",
        "views/stock_scrap_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "GPL-2",
}
