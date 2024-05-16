# -*- coding: utf-8 -*- account.journal

from odoo import api, fields, models, _


class camposDiariosRD(models.Model):
    _inherit = 'account.journal'

    itp_fecha_vencimiento = fields.Date(string='Fecha de vencimiento')
    itp_numero_autorizado = fields.Integer(string="Número Autorizado", default=1)
    itp_intervalo_aviso = fields.Integer(string="Notificar antes de", default=1,
                                        help="Notifica al usuario cuando esté próximo a alcanzar el máximo")



