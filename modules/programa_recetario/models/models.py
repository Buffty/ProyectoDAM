# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta

class recetas(models.Model):
    _name = 'programa_recetario.recetas'
    name = fields.Char()
    descripcion = fields.Char()
    tipo = fields.Char()
    dificultad = fields.Char()
    duracion = fields.Char()
    usuarios_id = fields.Many2one('res.partner')

class usuarios(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    passwd = fields.Char()
    is_app = fields.Boolean(default=True)
    recetas_id = fields.One2many('programa_recetario.recetas', 'usuarios_id', ondelete='cascade')