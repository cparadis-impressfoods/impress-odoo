# -*- coding: utf-8 -*-
{
    "name": "production_log_note",
    "version": "0.1.2",
    "summary": """ Backport of V18 feature where a note can be added to a production order""",
    "author": "Cédric Paradis",
    "website": "",
    "category": "Hidden",
    "depends": ["base", "web", "mrp_workorder"],
    "data": ["views/mrp_production_views.xml"],
    "assets": {
        "web.assets_backend": ["production_log_note/static/src/**/*"],
    },
    "installable": True,
    "license": "GPL-2",
}
