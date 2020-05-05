from odoo import models, fields, api, tools
from datetime import datetime, timedelta
import json

# ***************** CREAR CIUDADES **********************

class create_city(models.TransientModel):
    _name = 'medievol.create_city'

    def _default_player(self):
        jugador = self.env['res.partner'].browse(self._context.get('active_id'))
        print(jugador.name)
        return jugador

    player = fields.Many2one('res.partner', default=_default_player, readonly=True)
    region = fields.Many2one('medievol.region')
    state = fields.Selection([('i', "Elegir región"), ('f', "Finalizar región")], default='i')
    nombre = fields.Char()

    @api.multi
    def back(self):
        if self.state == 'f':
            self.state = 'i'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de ciudad',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def next(self):
        if self.state == 'i':
            self.state = 'f'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de ciudad',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def new(self):
        c_template = self.env.ref('medievol.city1')
        c = self.env['medievol.city'].create({
            'name': self.nombre,
            'image': c_template.image,
            'poblation': 100,
            'defense': 50,
            'quarry_id': self.env.ref('medievol.quarry1').id,
            'mine_id': self.env.ref('medievol.mine1').id,
            'farm_id': self.env.ref('medievol.farm1').id,
            'castle_id': self.env.ref('medievol.castle1').id,
            'infirmary_id': self.env.ref('medievol.infirmary0').id,
            'wall_id': self.env.ref('medievol.wall0').id,
            'barracks_id': self.env.ref('medievol.barracks0').id,
            'treasury_id': self.env.ref('medievol.treasury0').id,
            'forge_id': self.env.ref('medievol.forge0').id,
            'player_id': self.player.id,
            'region_id': self.region.id
        })
        for i in [1, 2, 3, 4]:
            if i < 4:
                p = self.env['medievol.means_city'].create({
                    'cantidad': 100,
                    'city_id': c.id,
                    'means_id': self.env.ref('medievol.means' + str(i)).id
                })
            else:
                p = self.env['medievol.means_city'].create({
                    'cantidad': 50,
                    'city_id': c.id,
                    'means_id': self.env.ref('medievol.means' + str(i)).id
                })


# ***************** CREAR GUERRAS *********************************

class type_soldiers(models.TransientModel):
    _name = 'medievol.type_soldiers'

    brujo = fields.Many2one('medievol.create_wars')
    tipo = fields.Many2one('medievol.soldiers')
    quantity = fields.Float()

class create_wars(models.TransientModel):
    _name = 'medievol.create_wars'

    def _default_city(self):
        return self.env['medievol.city'].browse(self._context.get('active_id'))

    def _default_player(self):
        player = self.env['medievol.city'].browse(self._context.get('active_id')).player_id
        return player
    def _get_date(self):
        date = datetime.now()
        return fields.Datetime.to_string(date)

    def _get_date_fin(self):
        date = datetime.now() + timedelta(hours=4)
        return fields.Datetime.to_string(date)

    city = fields.Many2one('medievol.city', default=_default_city, readonly=True)
    player = fields.Many2one('res.partner', default=_default_player, readonly=True)
    fecha_ini = fields.Datetime(default=_get_date)
    fecha_fin = fields.Datetime(default=_get_date_fin)
    soldiers_wars = fields.Many2many('medievol.soldiers_wars')

    tipo = fields.Many2one('medievol.soldiers')
    def _get_attack_domain(self):
        c = self._context.get('citys')
        if c:
          c = json.loads(c)
          return [('id','in',c)]

    city_attack = fields.Many2one('medievol.city', domain=_get_attack_domain)

    wiz_soldiers = fields.One2many('medievol.type_soldiers', 'brujo')
    quantity = fields.Float()
    state = fields.Selection([('i', "Selección Soldados"), ('c', "Ciudad a Atacar"), ('f', "Finalizar")],
                             default='i')

    @api.onchange('city')
    def _onchange_soldiers(self):
        for f in self:
            return {
                'domain': {'tipo': [('id', 'in', f.city.soldiers_city_id.soldiers_id.ids)]}
            }

    @api.multi
    def send_soldiers(self):
        for f in self:
            self.env['medievol.type_soldiers'].create({
                'brujo': f.id,
                'tipo': f.tipo.id,
                'quantity': f.quantity
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de Batallas',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }



    @api.multi
    def exit(self):
        return

    @api.multi
    def next(self):
        if self.state == 'i':
            self.state = 'c'
        elif self.state == 'c':
            self.state = 'f'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de Batallas',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'context': {'citys': json.dumps(self.env['medievol.city'].search([]).filtered(lambda r: r.id != self.city.id).ids)},
            'target': 'new'
        }


    @api.multi
    def back(self):
        if self.state == 'f':
            self.state = 'c'
        elif self.state == 'c':
            self.state = 'i'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de Batallas',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def new_battle(self):
        for f in self:
            soldados_cantidad = f.wiz_soldiers
            for soldiers in soldados_cantidad:
                batalla = self.env['medievol.wars'].create({})

                self.env['medievol.soldiers_wars'].create({
                    'cantidad': soldiers.quantity,
                    'soldiers_id': soldiers.tipo.id,
                    'city_id': f.city.id,
                    'city_attack_id': f.city_attack.id,
                    'batalla_id': batalla.id,
                    'player_id': f.player.id
                })

# ***************** CREAR SOLDADOS **********************

class create_soldiers(models.TransientModel):
    _name = 'medievol.create_soldiers'

    def _default_city(self):
        city = self.env['medievol.city'].browse(self._context.get('city_id'))
        return city

    city = fields.Many2one('medievol.city', default=_default_city, readonly=True)
    soldiers = fields.Many2one('medievol.soldiers')
    quantity = fields.Float()
    comprobar = fields.Boolean()
    cfoodsoldier = fields.Integer(readonly=True)
    cgoldsoldier = fields.Integer(readonly=True)
    cfoodcity = fields.Float(readonly=True)
    cgoldcity = fields.Float(readonly=True)

    state = fields.Selection([('i', "Selección Soldados"), ('c', "Gastos de Producción"), ('f', "Finalizar")],
                             default='i')

    @api.multi
    def new(self):
        c = self.env['medievol.recruit_soldiers'].create({
            'cantidad': self.quantity,
            'city_id': self.city.id,
            'soldiers_id': self.soldiers.id
        })
        encontrado = False
        soldados_ciudad = self.city.soldiers_city_id.search([])
        if len(soldados_ciudad) > 0:
            for sol in soldados_ciudad:
                if c.soldiers_id == sol.soldiers_id:
                    sol.cantidad = sol.cantidad + c.cantidad
                    encontrado = True

        if encontrado == False:
            soldier_new = self.env['medievol.soldiers_city'].create({
                'cantidad': c.cantidad,
                'city_id': c.city_id.id,
                'soldiers_id': c.soldiers_id.id
            })

        granja = self.env['medievol.farm'].search([])[0]
        tesoreria = self.env['medievol.treasury'].search([])[0]
        recursos = self.city.means_city_id
        for r in recursos:
            if r.means_id == granja.means_id:
                r.cantidad = r.cantidad - self.cfoodsoldier
            elif r.means_id == tesoreria.means_id:
                r.cantidad = r.cantidad - self.cgoldsoldier

    @api.multi
    def back(self):
        if self.state == 'f':
            self.state = 'c'
        elif self.state == 'c':
            self.state = 'i'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de Soldados',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def next(self):
        if self.state == 'i':
            self.state = 'c'
            soldado = self.soldiers
            self.cfoodsoldier = soldado.food * self.quantity
            self.cgoldsoldier = soldado.gold * self.quantity
            granja = self.env['medievol.farm'].search([])[0]
            tesoreria = self.env['medievol.treasury'].search([])[0]
            recursos = self.city.means_city_id
            for r in recursos:
                if r.means_id == granja.means_id:
                    self.cfoodcity = r.cantidad
                elif r.means_id == tesoreria.means_id:
                    self.cgoldcity = r.cantidad
            cantidadfood = self.cfoodcity - self.cfoodsoldier
            cantidadgold = self.cgoldcity - self.cgoldsoldier
            if cantidadfood >= 0 and cantidadgold >= 0:
                self.comprobar = True
            else:
                self.comprobar = False

        elif self.state == 'c':
            if self.comprobar:
                self.state = 'f'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Creación de Soldados',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }
