# -*- coding: utf-8 -*-
# from odoo import http


# class Impress-barcode(http.Controller):
#     @http.route('/impress-barcode/impress-barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/impress-barcode/impress-barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('impress-barcode.listing', {
#             'root': '/impress-barcode/impress-barcode',
#             'objects': http.request.env['impress-barcode.impress-barcode'].search([]),
#         })

#     @http.route('/impress-barcode/impress-barcode/objects/<model("impress-barcode.impress-barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('impress-barcode.object', {
#             'object': obj
#         })

