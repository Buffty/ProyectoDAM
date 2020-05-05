# -*- coding: utf-8 -*-
from odoo import http

# class ProgramaRecetario(http.Controller):
#     @http.route('/programa_recetario/programa_recetario/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/programa_recetario/programa_recetario/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('programa_recetario.listing', {
#             'root': '/programa_recetario/programa_recetario',
#             'objects': http.request.env['programa_recetario.programa_recetario'].search([]),
#         })

#     @http.route('/programa_recetario/programa_recetario/objects/<model("programa_recetario.programa_recetario"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('programa_recetario.object', {
#             'object': obj
#         })