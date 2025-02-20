# -*- coding: utf-8 -*-
{
    'name': 'Mrp_add_qc_note_shop_floor',
    'version': '17.0.0.1.0',
    'summary': """ Mrp_add_qc_note_shop_floor Summary """,
    'author': 'Cédric Paradis',
    'website': '',
    'category': 'Hidden',
    'depends': ['base', 'web', 'mrp_workorder'],
    'data': [
        
    ],'assets': {
              'web.assets_backend': [
                  'mrp_add_qc_note_shop_floor/static/src/**/*',
                  'mrp_add_qc_note_shop_floor/static/src/mrp_display/dialog/mrp_quality_check_confirmation_dialog.xml',
              ],
          },
    'installable': True,
    'license': 'GPL-2',
}
