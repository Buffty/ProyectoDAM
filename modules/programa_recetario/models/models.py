# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class recetas(models.Model):
    _name = 'programa_recetario.recetas'
    name = fields.Char()
    descripcion = fields.Char()
    tipo = fields.Char()
    dificultad = fields.Char()
    duracion = fields.Char()
    image = fields.Binary()
    image_medium = fields.Binary(compute='_medium_image',store=True)
    usuarios_id = fields.Many2one('res.partner')
    ingredientes_id = fields.One2many('programa_recetario.ingredientes', 'recetas_id', ondelete='cascade')

    @api.depends('image')
    def _medium_image(self):
        for f in self:
            image = f.image
            image_medium = tools.image_get_resized_images(image)
            f.image_medium = image_medium["image_medium"]


class ingredientes(models.Model):
    _name = 'programa_recetario.ingredientes'
    name = fields.Char()
    quantity = fields.Char()
    recetas_id = fields.Many2one('programa_recetario.recetas')

class usuarios(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    passwd = fields.Char()
    is_app = fields.Boolean()
    recetas_id = fields.One2many('programa_recetario.recetas', 'usuarios_id', ondelete='cascade')