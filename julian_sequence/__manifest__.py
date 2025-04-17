{
    "name": "Julian Sequence for MRP",
    "summary": """
Julian Sequence for MRP
=====================

Adds a 'Julian' sequence type for sequences. This sequence type creates a number based on the current date and YYDDD format.
This serial is also unique for each product, but not between products. Product A and Product B can share the 23321 serial but the same product cannot have the same serial. Depends on the context variable julian_product_id to be set.
The module also adds the context variable when creating a serial from the mrp.production form.
This sequence type overrides any other behavior from ir.sequence (size, padding, next_number, etc).

""",
    "author": "Cédric Paradis",
    "website": "https://github.com/cparadis-impressfoods/impress-odoo",
    "license": "GPL-2",
    "category": "Hidden",
    "version": "17.0.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "mrp", "stock"],
    "installable": True,
}
