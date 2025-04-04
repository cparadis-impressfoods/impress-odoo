# -*- coding: utf-8 -*-
{
    "name": "Impress Maintenance Quality Management",
    "version": "17.0.1.0.0",
    "summary": """ Impress Foods quality management for maintenance """,
    "description": """
    Adds functionalities to segregate maintenance by departement (Maintenance vs Quality Control)
    """,
    "author": "Cédric Paradis",
    "website": "",
    "category": "Maintenance",
    "depends": [
        "base",
        "maintenance_worksheet",
        "base_maintenance",
        "quality",
    ],
    "data": [
        "data/team_tags.xml",
        "security/maintenance.xml",
        "security/ir.model.access.csv",
        "views/maintenance_equipment_category_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/maintenance_team_tag_views.xml",
        "views/maintenance_team_views.xml",
        "views/quality/maintenance_request_quality_views.xml",
        "views/quality/maintenance_equipment_quality_action.xml",
        "views/menus.xml",
    ],
    "application": True,
    "installable": True,
    "license": "GPL-2",
}
