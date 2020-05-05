# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta

class recetas(models.Model):
     _name = 'recetario.recetas'
     nombre = fields.Char()
     descripcion = fields.Char()
     tipo = fields.Char()
     dificultad = fields.Char()
     duracion = fields.Char()
     usuario_id = fields.Many2one('res.partner')

