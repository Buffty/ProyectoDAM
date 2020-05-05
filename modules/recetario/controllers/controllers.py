# -*- coding: utf-8 -*-
from odoo import http

# class Recetario(http.Controller):
#     @http.route('/recetario/recetario/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recetario/recetario/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('recetario.listing', {
#             'root': '/recetario/recetario',
#             'objects': http.request.env['recetario.recetario'].search([]),
#         })

#     @http.route('/recetario/recetario/objects/<model("recetario.recetario"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recetario.object', {
#             'object': obj
#         })