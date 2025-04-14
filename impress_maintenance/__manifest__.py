# -*- coding: utf-8 -*-
{
    "name": "Impress Maintenance",
    "version": "17.0.0.0.1",
    "summary": """ Impress_maintenance Summary """,
    "author": "Cédric Paradis",
    "website": "",
    "category": "Hidden",
    "depends": ["base", "hr_maintenance", "base_maintenance"],
    "data": [
        "views/hr_employee_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/maintenance_stage_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "GPL-2",
}
