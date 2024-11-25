# -*- coding: utf-8 -*-
{
    'name': "Julian Sequence for MRP",

    'summary': "Allows the creation of sequences based on the YYDDD format",

    'description': """
Julian Sequence for MRP
=====================

Adds a 'Julian' sequence type for sequences. This sequence type creates a number based on the current date and YYDDD format.
This serial is also unique for each product, but not between products. Product A and Product B can share the 23321 serial but the same product cannot have the same serial. Depends on the context variable julian_product_id to be set. 
The module also adds the context variable when creating a serial from the mrp.production form. 
This sequence type overrides any other behavior from ir.sequence (size, padding, next_number, etc).

""",
    'author': "Cédric Paradis",
    'website': "",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'stock'],
    'installable': True,

}
