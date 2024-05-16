# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_invoice_number = fields.Boolean('Show POS Invoice Number', default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_invoice_number = fields.Boolean(related='pos_config_id.pos_invoice_number',readonly=False)