# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class facturaRepDomPOS(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_invoice_mgp(self, id):
        # res = super(facturaRepDomPOS, self).get_invoice_mgp(id)

        if id:
            pos_id = self.sudo().search([('pos_reference', '=', id)])
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            invoice_id = self.env['account.move'].sudo().search([('ref', '=', pos_id.name), ('move_type','=','out_invoice')])

            nombre_factura = invoice_id.name
            # print('Datos Journal ', invoice_id.journal_id)
            if len(invoice_id.journal_id) == 1:
                nombre_diario = invoice_id.journal_id.name
            else:
                nombre_diario = 'Aquí está el clavo' + id

                my_pos_order = self.env['pos.order'].sudo().search([('pos_reference', '=', id)])
                my_invoice = self.env['account.move'].sudo().search([('ref', '=', my_pos_order.name)])
                nombre_diario = my_invoice.journal_id.name
                nombre_factura = my_invoice.name


            # fecha_vencimiento_dgii = invoice_id.journal_id.itp_fecha_vencimiento

            return {
                'invoice_id': invoice_id.id,
                'invoice_name': nombre_factura,
                'base_url': base_url,
                'nombre_diario': nombre_diario,
                'direccion_tienda': "Ciudad",
            }

