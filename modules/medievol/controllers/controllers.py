# -*- coding: utf-8 -*-
from odoo import http

# class Medievol(http.Controller):
#     @http.route('/medievol/medievol/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medievol/medievol/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('medievol.listing', {
#             'root': '/medievol/medievol',
#             'objects': http.request.env['medievol.medievol'].search([]),
#         })

#     @http.route('/medievol/medievol/objects/<model("medievol.medievol"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medievol.object', {
#             'object': obj
#         })