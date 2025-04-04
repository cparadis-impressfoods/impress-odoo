# -*- coding: utf-8 -*-
{
    "name": "Maintenance_quality",
    "version": "17.0.0.0.1",
    "summary": """ Maintenance_quality Summary """,
    "author": "Cédric Paradis",
    "website": "",
    "category": "Hidden",
    "depends": [
        "quality_control",
        "mrp_maintenance",
        "maintenance_worksheet",
        "mrp_workorder",
    ],
    "data": [
        "views/maintenance_equipment_category_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/mrp_workcenter_views.xml",
        "views/quality_alert_views.xml",
        "views/quality_check_views.xml",
        "views/quality_point_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "GPL-2",
}
