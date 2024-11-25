# -*- coding: utf-8 -*-
# from odoo import http


# class ./addons/julianSequence(http.Controller):
#     @http.route('/./addons/julian_sequence/./addons/julian_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons/julian_sequence/./addons/julian_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons/julian_sequence.listing', {
#             'root': '/./addons/julian_sequence/./addons/julian_sequence',
#             'objects': http.request.env['./addons/julian_sequence../addons/julian_sequence'].search([]),
#         })

#     @http.route('/./addons/julian_sequence/./addons/julian_sequence/objects/<model("./addons/julian_sequence../addons/julian_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons/julian_sequence.object', {
#             'object': obj
#         })

