{
    "name": "impress_barcode",
    "summary": """
        Customizations to barcode app
    """,
    "author": "Cédric Paradis",
    "website": "https://github.com/cparadis-impressfoods/impress-odoo",
    "category": "Hidden",
    "version": "17.0.0.1.2",
    "license": "GPL-2",
    "depends": ["base", "stock", "sale_management", "stock_barcode"],
    "data": [
        "views/stock_picking_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "impress_barcode/static/src/components/move.xml",
            "impress_barcode/static/src/components/move.js",
            "impress_barcode/static/src/components/line.xml",
            "impress_barcode/static/src/components/main.js",
            "impress_barcode/static/src/components/main.xml",
            "impress_barcode/static/src/main.xml",
            "impress_barcode/static/src/**/*.js",
        ],
    },
}
