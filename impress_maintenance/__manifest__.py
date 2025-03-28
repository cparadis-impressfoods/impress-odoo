# -*- coding: utf-8 -*-
{
    'name': 'Impress_maintenance',
    'version': '17.0.0.0.1',
    'summary': """ Impress_maintenance Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Maintenance',
    'depends': ['base','maintenance_worksheet', 'quality', 'hr_maintenance', 'documents'],
    "data": [
        "data/team_tags.xml",
        "security/ir.model.access.csv",
        "views/maintenance_equipment_action.xml",
        "views/maintenance_equipment_category_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/maintenance_team_tag_views.xml",
        "views/maintenance_team_views.xml",
        'views/quality/maintenance_request_quality_views.xml',
        'views/quality/maintenance_equipment_quality_action.xml',
        "views/menus.xml",
        "security/maintenance.xml",
        'data/document_folder.xml',
        
    ],
    
    'application': True,
    'installable': True,
    'license': 'GPL-2',
}
