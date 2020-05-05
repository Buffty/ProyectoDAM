# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta

class recetas(models.Model):
    _name = 'programa_recetario.recetas'
    name = fields.Char()
