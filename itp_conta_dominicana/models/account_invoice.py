# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class facturasRD(models.Model):
    _inherit = 'account.move'

    tipo_de_ingreso = fields.Many2one('tipo.ingreso', required=True,
                                      default=lambda self: self._default_tipo_ingreso())
    tipo_de_egreso = fields.Many2one('tipo.egreso', required=True,
                                     default=lambda self: self._default_tipo_egreso())
    itp_ncf_proveedor = fields.Char(string="NCF", size=13, copy=False)
    itp_vat_factura = fields.Char(compute='_get_vat_factura', store=True)
    # Para notas de crédito
    itp_ncf_origen = fields.Char(string="NCF Origen", size=13)
    itp_rnc_origen = fields.Char(string="RNC Origen")

    def _default_tipo_ingreso(self):
        # Return the default value based on your logic
        return self.env['tipo.ingreso'].search([], limit=1)

    def _default_tipo_egreso(self):
        # Return the default value based on your logic
        return self.env['tipo.egreso'].search([], limit=1)

    def action_reverse(self):
        res = super(facturasRD, self).action_reverse()

        if self.move_type == 'out_invoice':
            # Nota de crédito
            self.itp_ncf_origen = self.name
            self.itp_rnc_origen = self.itp_vat_factura

        return res


    def action_post(self):
        res = super(facturasRD, self).action_post()

        if self.move_type == 'out_invoice':
            if not self.partner_id.vat:
                raise ValidationError("Error al registrar factura: verifique que"
                                      " el cliente tenga identificador fiscal")

            self.validar_diario()
            self.validar_numero()
            # self.validar_ncf()

            if not self.itp_ncf_proveedor:
                self.itp_ncf_proveedor = self.name

        if self.move_type == 'in_invoice':
            if not self.itp_ncf_proveedor:
                if self.name[:3] in ('B11', 'B13', 'B14'):
                    self.itp_ncf_proveedor = self.name
                else:
                    raise ValidationError("Error: debe ingresar NCF de proveedor")

        if self.move_type == 'out_refund':
            self.itp_ncf_proveedor = self.name

            if not self.itp_ncf_proveedor:
                if self.name[:3] not in ('B02', 'INV'):
                    raise ValidationError("Error: debe ingresar NCF de proveedor")

            # No permite continuar si ingresa B04 y B02
            prefijo = self.itp_ncf_proveedor[:3]

            # if prefijo in ('B04', 'B02'):
            #     raise ValidationError("Error al confirmar factura: verifique que el código de NCF sea permitido")

        return res

    def validar_numero(self):
        # Validar número máximo autorizado por la DGII
        numero_maximo = self.journal_id.itp_numero_autorizado
        secuencia_actual = self.journal_id.sequence_id.number_next_actual
        intervalo = self.journal_id.itp_intervalo_aviso
        vigentes = numero_maximo - secuencia_actual

        if vigentes <= int(intervalo):
            self.action_notification()

        if vigentes <= 0:
            raise ValidationError("ERROR: No cuenta con documentos autorizados.")


        #if intervalo < vigentes:

    def action_notification(self):
        self.env['bus.bus']._sendone(self.env.user.partner_id,
                                     "simple_notification",
                                     {
                                         "title": "La cantidad de documentos habilitados está próximo a terminarse",
                                         "message": "Mensaje de notificación",
                                         'type': 'warning',  # success | warning | danger
                                         'sticky': False,
                                     }
                                     )

        return True

    def validar_diario(self):

        if self.journal_id:

            if self.journal_id.type in ('sale', 'purchase'):

                if not self.journal_id.itp_fecha_vencimiento:
                    raise ValidationError("Debe registrar una fecha de vencimiento en el diario respectivo")

                # Validar fecha de caducidad
                if self.invoice_date > self.journal_id.itp_fecha_vencimiento:
                    raise ValidationError("Error al confirmar factura: verifique la fecha de"
                                          " vencimiento para este tipo de facturas")
            # elif codigo_diario == 'B02':
            #
            # else:
            #    raise ValidationError("no existe código de diario establecido para venta")

        return True

    def validar_ncf(self):
        if not self.partner_id.vat:
            raise ValidationError("Error al registrar factura: verifique que"
                                  " el cliente tenga identificador fiscal")


    @api.depends('partner_id', 'partner_id.vat')
    def _get_vat_factura(self):
        for record in self:
            id_fiscal = record.partner_id.vat
            record.itp_vat_factura = id_fiscal
