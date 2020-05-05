# -*- coding: utf-8 -*-

from odoo import models, fields, api

class recetas(models.Model):
    _name = 'programa_recetario.recetas'
    name = fields.Char()

class usuarios(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    passwd = fields.Char()
    is_app = fields.Boolean()