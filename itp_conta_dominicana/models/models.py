# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tipoIngreso(models.Model):
    _name = 'tipo.ingreso'

    _description = 'Tipo de ingreso'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tipo de Ingreso')
    activo = fields.Boolean(string="Activo", default=True)


class tipoEgreso(models.Model):
    _name = 'tipo.egreso'

    _description = 'Tipo de egreso'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tipo de Egreso')
    activo = fields.Boolean(string="Activo", default=True)

#class diariosRDom(models.Model):
#    _inherit = 'account.journal'

#    itp_fecha_vencimiento = fields.Date(string="Fecha de vencimiento")

# class itp_conta_dominicana(models.Model):
#     _name = 'itp_conta_dominicana.itp_conta_dominicana'
#     _description = 'itp_conta_dominicana.itp_conta_dominicana'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
