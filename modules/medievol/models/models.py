# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta

class city(models.Model):
    _name = 'medievol.city'
    name = fields.Char()
    image = fields.Binary()
    image_medium = fields.Binary(compute='_medium_image',store=True)
    poblation = fields.Float()
    defense = fields.Float()

    quarry_id = fields.Many2one('medievol.quarry')
    quarry_datos = fields.Many2many( 'medievol.quarry', compute='_get_resources')

    mine_id = fields.Many2one('medievol.mine')
    mine_datos = fields.Many2many('medievol.mine', compute='_get_resources')

    farm_id = fields.Many2one('medievol.farm')
    farm_datos = fields.Many2many('medievol.farm', compute='_get_resources')

    castle_id = fields.Many2one('medievol.castle')
    castle_datos = fields.Many2many('medievol.castle', compute='_get_resources')

    infirmary_id = fields.Many2one('medievol.infirmary')
    infirmary_datos = fields.Many2many('medievol.infirmary', compute='_get_resources')

    forge_id = fields.Many2one('medievol.forge')
    forge_datos = fields.Many2many('medievol.forge', compute='_get_resources')

    treasury_id = fields.Many2one('medievol.treasury')
    treasury_datos = fields.Many2many('medievol.treasury', compute='_get_resources')

    barracks_id = fields.Many2one('medievol.barracks')
    barracks_datos = fields.Many2many('medievol.barracks', compute='_get_resources')

    wall_id = fields.Many2one('medievol.wall')
    wall_datos = fields.Many2many('medievol.wall', compute='_get_resources')

    region_id = fields.Many2one('medievol.region')
    player_id = fields.Many2one('res.partner')
    means_city_id = fields.One2many('medievol.means_city','city_id')
    soldiers_city_id = fields.One2many('medievol.soldiers_city','city_id')
    recruit_soldiers_id = fields.One2many('medievol.recruit_soldiers', 'city_id')
    graficos_id = fields.One2many('medievol.grafico','city_id')
    soldiers_wars_id = fields.One2many('medievol.soldiers_wars','city_id')

    @api.depends('quarry_id','mine_id','farm_id','castle_id','infirmary_id','forge_id','treasury_id','barracks_id','wall_id')
    def _get_resources(self):
        for f in self:
            f.quarry_datos = [f.quarry_id.id]
            f.mine_datos = [f.mine_id.id]
            f.farm_datos = [f.farm_id.id]
            f.castle_datos = [f.castle_id.id]
            f.infirmary_datos = [f.infirmary_id.id]
            f.forge_datos = [f.forge_id.id]
            f.treasury_datos = [f.treasury_id.id]
            f.barracks_datos = [f.barracks_id.id]
            f.wall_datos = [f.wall_id.id]

    @api.onchange('poblation')
    def _onchange_poblation(self):
        for r in self:
            c = r.castle_id
            if r.poblation > c.limit_poblation:
                r.poblation = c.limit_poblation

    @api.constrains('poblation')
    def _check_poblation(self):
        for r in self:
            c = r.castle_id
            if r.poblation > c.limit_poblation:
                raise ValidationError("Fallo a la hora de aumentar poblacion")

    @api.depends('image')
    def _medium_image(self):
        for f in self:
            image = f.image
            image_medium = tools.image_get_resized_images(image)
            f.image_medium = image_medium["image_medium"]

    @api.multi
    def _level_up_quarry(self):
        for r in self:
            piedra = r.quarry_id
            hierro = r.mine_id
            cantidadpiedra = piedra.stone
            cantidadhierro = piedra.iron
            recursos = r.means_city_id
            for means in recursos:
                if means.means_id == piedra.means_id:
                    cantidadpiedra = cantidadpiedra - means.cantidad
                elif means.means_id == hierro.means_id:
                    cantidadhierro = cantidadhierro - means.cantidad
            if cantidadhierro <= 0.0 and cantidadpiedra <= 0.0:
                cantidadpiedra = piedra.stone
                cantidadhierro = piedra.iron
                for means in recursos:
                    if means.means_id == piedra.means_id:
                        means.cantidad = means.cantidad - cantidadpiedra
                    elif means.means_id == hierro.means_id:
                        means.cantidad = means.cantidad - cantidadhierro
                if r.quarry_id.lvl+1 < 6:
                    r.quarry_id = self.env.ref('medievol.quarry'+str(r.quarry_id.lvl+1))

    @api.multi
    def _level_up_mine(self):
        for r in self:
            piedra = r.quarry_id
            hierro = r.mine_id
            cantidadpiedra = hierro.stone
            cantidadhierro = hierro.iron
            recursos = r.means_city_id
            for means in recursos:
                if means.means_id == piedra.means_id:
                    cantidadpiedra = cantidadpiedra - means.cantidad
                elif means.means_id == hierro.means_id:
                    cantidadhierro = cantidadhierro - means.cantidad
            if cantidadhierro <= 0.0 and cantidadpiedra <= 0.0:
                cantidadpiedra = hierro.stone
                cantidadhierro = hierro.iron
                for means in recursos:
                    if means.means_id == piedra.means_id:
                        means.cantidad = means.cantidad - cantidadpiedra
                    elif means.means_id == hierro.means_id:
                        means.cantidad = means.cantidad - cantidadhierro
                if r.mine_id.lvl+1 < 6:
                    r.mine_id = self.env.ref('medievol.mine'+str(r.mine_id.lvl+1))

    @api.multi
    def _level_up_farm(self):
        for r in self:
            piedra = r.quarry_id
            hierro = r.mine_id
            granja = r.farm_id
            cantidadpiedra = granja.stone
            cantidadhierro = granja.iron
            recursos = r.means_city_id
            for means in recursos:
                if means.means_id == piedra.means_id:
                    cantidadpiedra = cantidadpiedra - means.cantidad
                elif means.means_id == hierro.means_id:
                    cantidadhierro = cantidadhierro - means.cantidad
            if cantidadhierro <= 0.0 and cantidadpiedra <= 0.0:
                cantidadpiedra = granja.stone
                cantidadhierro = granja.iron
                for means in recursos:
                    if means.means_id == piedra.means_id:
                        means.cantidad = means.cantidad - cantidadpiedra
                    elif means.means_id == hierro.means_id:
                        means.cantidad = means.cantidad - cantidadhierro
                if r.farm_id.lvl+1 < 6:
                    r.farm_id = self.env.ref('medievol.farm'+str(r.farm_id.lvl+1))

    @api.multi
    def _level_up_castle(self):
        for r in self:
            piedra = r.quarry_id
            hierro = r.mine_id
            castillo = r.castle_id
            cantidadpiedra = castillo.stone
            cantidadhierro = castillo.iron
            recursos = r.means_city_id
            for means in recursos:
                if means.means_id == piedra.means_id:
                    cantidadpiedra = cantidadpiedra - means.cantidad
                elif means.means_id == hierro.means_id:
                    cantidadhierro = cantidadhierro - means.cantidad
            if cantidadhierro <= 0.0 and cantidadpiedra <= 0.0:
                cantidadpiedra = castillo.stone
                cantidadhierro = castillo.iron
                for means in recursos:
                    if means.means_id == piedra.means_id:
                        means.cantidad = means.cantidad - cantidadpiedra
                    elif means.means_id == hierro.means_id:
                        means.cantidad = means.cantidad - cantidadhierro
                if r.castle_id.lvl+1 < 6:
                    r.castle_id = self.env.ref('medievol.castle'+str(r.castle_id.lvl+1))

    @api.multi
    def _level_up_barracks(self):
        for r in self:
            if r.barracks_id.lvl + 1 < 6:
                r.barracks_id = self.env.ref('medievol.barracks' + str(r.barracks_id.lvl + 1))

    @api.multi
    def _level_up_treasury(self):
        for r in self:
             if r.treasury_id.lvl + 1 < 6:
                 r.treasury_id = self.env.ref('medievol.treasury' + str(r.treasury_id.lvl + 1))

    @api.multi
    def _level_up_infirmary(self):
        for r in self:
            if r.infirmary_id.lvl + 1 < 6:
                r.infirmary_id = self.env.ref('medievol.infirmary' + str(r.infirmary_id.lvl + 1))

    @api.multi
    def _level_up_forge(self):
        for r in self:
            if r.forge_id.lvl + 1 < 6:
                r.forge_id = self.env.ref('medievol.forge' + str(r.forge_id.lvl + 1))

    @api.multi
    def _level_up_wall(self):
        for r in self:
            if r.wall_id.lvl + 1 < 6:
                r.wall_id = self.env.ref('medievol.wall' + str(r.wall_id.lvl + 1))

class quarry(models.Model):
    _name = 'medievol.quarry'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    stone = fields.Integer()
    iron = fields.Integer()
    lvl = fields.Integer()
    construir = fields.Boolean(compute='_can_building',store=True)
    production = fields.Float()
    means_id = fields.Many2one('medievol.means')
    city_id = fields.One2many('medievol.city', 'quarry_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def _can_building(self):
        for g in self:
            r = g.city_id.means_city_id
            piedra = g.city_id.quarry_id
            hierro = g.city_id.mine_id
            recursospedra = r.search([]).filtered(lambda r: r.means_id == piedra).cantidad
            recursoshierro = r.search([]).filtered(lambda r: r.means_id == hierro).cantidad
            if (recursospedra - g.stone) <= 0 and (recursoshierro - g.iron) <= 0:
                g.construir = True
            else:
                g.construir = False

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_quarry()


class mine(models.Model):
    _name = 'medievol.mine'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    stone = fields.Integer()
    iron = fields.Integer()
    lvl = fields.Integer()
    production = fields.Float()
    means_id = fields.Many2one('medievol.means')
    city_id = fields.One2many('medievol.city','mine_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_mine()

class farm(models.Model):
    _name = 'medievol.farm'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    stone = fields.Integer()
    iron = fields.Integer()
    lvl = fields.Integer()
    production = fields.Float()
    means_id = fields.Many2one('medievol.means')
    city_id = fields.One2many('medievol.city','farm_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_farm()

class castle(models.Model):
    _name = 'medievol.castle'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    stone = fields.Integer()
    iron = fields.Integer()
    lvl = fields.Integer()
    limit_poblation = fields.Integer()
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings', 'castle_id')
    city_id = fields.One2many('medievol.city','castle_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_castle()

class infirmary(models.Model):
    _name = 'medievol.infirmary'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    lvl = fields.Integer()
    stone = fields.Integer()
    iron = fields.Integer()
    limit_injureds = fields.Integer()
    city_id = fields.One2many('medievol.city','infirmary_id')
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings', 'infirmary_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_infirmary()

class forge(models.Model):
    _name = 'medievol.forge'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    lvl = fields.Integer()
    stone = fields.Integer()
    iron = fields.Integer()
    city_id = fields.One2many('medievol.city','forge_id')
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings', 'forge_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_forge()

class treasury(models.Model):
    _name = 'medievol.treasury'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    lvl = fields.Integer()
    stone = fields.Integer()
    iron = fields.Integer()
    production = fields.Float()
    means_id = fields.Many2one('medievol.means')
    city_id = fields.One2many('medievol.city','treasury_id')
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings', 'treasury_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_treasury()

class barracks(models.Model):
    _name = 'medievol.barracks'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    lvl = fields.Integer()
    stone = fields.Integer()
    iron = fields.Integer()
    limit_warriors = fields.Integer()
    city_id = fields.One2many('medievol.city','barracks_id')
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings', 'barracks_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_barracks()

class wall(models.Model):
    _name = 'medievol.wall'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    lvl = fields.Integer()
    stone = fields.Integer()
    iron = fields.Integer()
    defense = fields.Float()
    city_id = fields.One2many('medievol.city','wall_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

    @api.multi
    def level_up(self):
        for r in self:
            r.city_id._level_up_wall()

# ********************************* SOLDADOS *********************************

class recruit_soldiers(models.Model):
    _name = 'medievol.recruit_soldiers'
    cantidad = fields.Float()
    city_id = fields.Many2one('medievol.city')
    soldiers_id = fields.Many2one('medievol.soldiers')

class soldiers(models.Model):
    _name = 'medievol.soldiers'
    name = fields.Char()
    attack = fields.Integer()
    defense = fields.Integer()
    food = fields.Integer()
    gold = fields.Integer()
    time = fields.Integer()
    consum = fields.Integer()
    type = fields.Selection([('1','Infantería'),('2','Alabardero'),('3','Arquero'),('4','Caballería')])
    life = fields.Integer()
    soldiers_city_id = fields.One2many('medievol.soldiers_city','soldiers_id')
    recruit_soldiers_id = fields.One2many('medievol.recruit_soldiers','soldiers_id')
    soldiers_wars_id = fields.One2many('medievol.soldiers_wars','soldiers_id')

class soldiers_city(models.Model):
    _name = 'medievol.soldiers_city'
    cantidad = fields.Float()
    city_id = fields.Many2one('medievol.city')
    soldiers_id = fields.Many2one('medievol.soldiers')

# ********************************* VENTAS *********************************

# class ventas_player(models.Model):
#     _inherit = 'sale.order'
#     _name = 'sale.order'
#
#     venta_juego = fields.Boolean()
#     incremento = fields.Integer()


class productos_game(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    juego = fields.Boolean()

# ********************************* JUGADOR *********************************

class player(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    def _default_name(self):
        return 'Default Name'
    region_id = fields.Many2many('medievol.region')
    city_id = fields.One2many('medievol.city','player_id', ondelete='cascade')
    soldiers_wars_id = fields.One2many('medievol.soldiers_wars','player_id')

    def update_means(self):
        p = self.env['res.partner'].search([]).filtered(lambda r: len(r.city_id) > 0)
        for player in p:
            c = player.city_id
            # SE RECORREN LAS CIUDADES
            for ciudad in c:
                r = ciudad.means_city_id
                region = ciudad.region_id
                cantera = ciudad.quarry_id
                granja = ciudad.farm_id
                mina = ciudad.mine_id
                soldados = ciudad.soldiers_city_id
                tesoreria = ciudad.treasury_id
                for recursos in r:
                    if cantera.means_id == recursos.means_id:
                        if region.id == 2:
                            recursos.cantidad = cantera.production + recursos.cantidad + ((cantera.production*20)/100)
                        elif region.id == 1:
                            recursos.cantidad = cantera.production + recursos.cantidad - ((cantera.production*10)/100)
                        elif region.id == 3:
                            recursos.cantidad = cantera.production + recursos.cantidad - ((cantera.production*20)/100)

                    elif granja.means_id == recursos.means_id:
                        if region.id == 1:
                            recursos.cantidad = granja.production + recursos.cantidad + ((granja.production * 25) / 100)
                        else:
                            recursos.cantidad = granja.production + recursos.cantidad
                    elif mina.means_id == recursos.means_id:
                        if region.id == 2:
                            recursos.cantidad = recursos.cantidad + mina.production - ((mina.production*20)/100)
                        elif region.id == 1:
                            recursos.cantidad = mina.production + recursos.cantidad - ((mina.production*10) / 100)
                        elif region.id == 3:
                            recursos.cantidad = mina.production + recursos.cantidad + ((mina.production * 20) / 100)
                    elif tesoreria.means_id == recursos.means_id:
                        recursos.cantidad = recursos.cantidad + tesoreria.production
                # COMPROBACIÓN DE SOLDADOS
                for soldier in soldados:
                    cantfood = soldier.soldiers_id.consum
                    for recursos in r:
                        if granja.means_id == recursos.means_id:
                            recursos.cantidad = recursos.cantidad - (cantfood*soldier.cantidad)
                # SE CREAN LOS GRÁFICOS
                self.env['medievol.grafico'].create({
                    'city_id': ciudad.id
                })



    @api.multi
    def add_city(self):
        for p in self:
            c_template=self.env.ref('medievol.city1')
            c = self.env['medievol.city'].create({
                'name' : 'Change the name (new)',
                'image' : c_template.image,
                'poblation' : 100,
                'defense' : 50,
                'quarry_id': self.env.ref('medievol.quarry1').id,
                'mine_id' : self.env.ref('medievol.mine1').id,
                'farm_id' : self.env.ref('medievol.farm1').id,
                'castle_id' : self.env.ref('medievol.castle1').id,
                'infirmary_id': self.env.ref('medievol.infirmary0').id,
                'wall_id': self.env.ref('medievol.wall0').id,
                'barracks_id': self.env.ref('medievol.barracks0').id,
                'treasury_id': self.env.ref('medievol.treasury0').id,
                'forge_id': self.env.ref('medievol.forge0').id,
                'player_id' : p.id,
                'region_id' : c_template.region_id.id
            })
            for i in [1, 2, 3, 4]:
                if i < 4:
                    p = self.env['medievol.means_city'].create({
                        'cantidad' : 100,
                        'city_id' : c.id,
                        'means_id': self.env.ref('medievol.means'+str(i)).id
                    })
                else:
                    p = self.env['medievol.means_city'].create({
                        'cantidad': 50,
                        'city_id': c.id,
                        'means_id': self.env.ref('medievol.means' + str(i)).id
                    })



# ********************************* REGION *********************************

class region(models.Model):
    _name = 'medievol.region'
    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute='_small_image', store=True)
    player_id = fields.Many2many('res.partner')
    city_id = fields.One2many('medievol.city','region_id')
    city_id_kanban = fields.One2many(related='city_id')

    @api.depends('image')
    def _small_image(self):
        for f in self:
            image = f.image
            image_small = tools.image_get_resized_images(image)
            f.image_small = image_small["image_small"]

# ********************************* BATALLAS *********************************

class soldiers_wars(models.Model):
    _name = 'medievol.soldiers_wars'
    cantidad = fields.Integer()
    soldiers_id = fields.Many2one('medievol.soldiers')
    city_id = fields.Many2one('medievol.city')
    city_attack_id = fields.Many2one('medievol.city')
    batalla_id = fields.Many2one('medievol.wars')
    player_id = fields.Many2one('res.partner')

class batalla(models.Model):
    _name = 'medievol.wars'
    def _get_date(self):
        date = datetime.now()
        return fields.Datetime.to_string(date)

    def _get_date_fin(self):
        date = datetime.now()+timedelta(hours=4)
        return fields.Datetime.to_string(date)

    fecha_ini = fields.Datetime(default=_get_date)
    fecha_fin = fields.Datetime(default=_get_date_fin)
    soldiers_wars_id = fields.One2many('medievol.soldiers_wars','batalla_id')

# ********************************* GRÁFICO **********************************

class grafico(models.Model):
    _name = 'medievol.grafico'
    city_id = fields.Many2one('medievol.city')
    food = fields.Float(compute='_get_compute_means',store=True)
    iron = fields.Float(compute='_get_compute_means', store=True)
    stone = fields.Float(compute='_get_compute_means', store=True)
    foodsoldiers = fields.Float(compute='_get_compute_means', store=True)
    date = fields.Char(default=lambda self: fields.Datetime.now())

    @api.depends('food','iron','stone','foodsoldiers')
    def _get_compute_means(self):
        for grafico in self:
            grafico.food = grafico.city_id.farm_id.production
            grafico.iron = grafico.city_id.mine_id.production
            grafico.stone = grafico.city_id.quarry_id.production
            soldados = grafico.city_id.soldiers_city_id
            for soldier in soldados:
                cantfood = soldier.soldiers_id.consum
                grafico.foodsoldiers = grafico.foodsoldiers + (cantfood * soldier.cantidad)

# ********************************* RECURSOS *********************************

class means(models.Model):
    _name = 'medievol.means'
    name = fields.Char()
    quarry_id = fields.One2many('medievol.quarry','means_id')
    mine_id = fields.One2many('medievol.mine','means_id')
    farm_id = fields.One2many('medievol.farm','means_id')
    treasury_id = fields.One2many('medievol.treasury','means_id')
    means_city_id = fields.One2many('medievol.means_city','means_id')

class means_city(models.Model):
    _name = 'medievol.means_city'
    cantidad = fields.Float()
    city_id = fields.Many2one('medievol.city')
    means_id = fields.Many2one('medievol.means')

# ********************************* INVESTIGACIONES *********************************

class investigation(models.Model):
    _name = 'medievol.investigation'
    name = fields.Char()
    description = fields.Text()
    increment = fields.Integer()
    investigation_buildings_id = fields.One2many('medievol.investigation_buildings','investigation_id')

class investigation_buidings(models.Model):
    _name = 'medievol.investigation_buildings'
    tipo = fields.Selection([('1','Forja'),('2','Enfermería'),('3','Barracones'),('4','Tesorería'),('5','Castillo')])
    duration = fields.Float()
    investigation_id = fields.Many2one('medievol.investigation')
    castle_id = fields.Many2one('medievol.castle')
    barracks_id = fields.Many2one('medievol.barracks')
    treasury_id = fields.Many2one('medievol.treasury')
    forge_id = fields.Many2one('medievol.forge')
    infirmary_id = fields.Many2one('medievol.infirmary')