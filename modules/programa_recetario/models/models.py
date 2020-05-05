# -*- coding: utf-8 -*-

from odoo import models, fields, api

class recetas(models.Model):
    _name = 'programa_recetario.recetas'
    name = fields.Char()
