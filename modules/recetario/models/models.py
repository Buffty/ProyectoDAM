# -*- coding: utf-8 -*-

from odoo import models, fields, api

class recetario(models.Model):
     _name = 'recetario.recetas'

     nombre = fields.Char()
     descripcion = fields.Char()
     tipo = fields.Char()
     dificultad = fields.Char()
     duracion = fields.Char()
     usuario_id = fields.Many2one('res.partner')


class usuario(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    passwd = fields.Char()

    id_recetario = fields.One2many('recetario.recetas','usuario_id',ondelete='cascade')
    aplicacion = fields.Boolean(default=True)


