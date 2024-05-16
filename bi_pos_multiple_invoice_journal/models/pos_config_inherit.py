# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp


class MultipleinvoicePayment(models.Model):
    _inherit = 'pos.config'

    def setup_invoice_journal(self, company):
        for pos_config in self:
            invoice_journal_id = pos_config.invoice_journal_id or self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', company.id)], limit=1)
            if invoice_journal_id:
                pos_config.write({'invoice_journal_id': [(6, 0, invoice_journal_id.ids)]})
            else:
                pos_config.write({'module_account': False})

    def _default_invoice_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id)], limit=1)

    invoice_journal_id = fields.Many2many(
            'account.journal', string='Invoice Journal',
            domain=[('type', '=', 'sale')],
            help="Accounting journal used to create invoices.",
            default=_default_invoice_journal)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_invoice_journal_id = fields.Many2many(related='pos_config_id.invoice_journal_id', readonly=False)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        new_model = 'account.journal'
        if new_model not in result:
            result.append(new_model)
        return result


    def _loader_params_account_journal(self):
        return {
            'search_params': {
                'domain': [('id', 'in', self.config_id.invoice_journal_id.ids)],
                'fields': [],
            }
        }

    def _get_pos_ui_account_journal(self, params):
        return self.env['account.journal'].search_read(**params['search_params'])

class Superforjournalid(models.Model):
    _inherit = 'pos.order'

    multi_id = fields.Many2one('account.journal', string='Invoice Journal ID')

    @api.model
    def _order_fields(self, ui_order):
        result = super(Superforjournalid, self)._order_fields(ui_order)
        if 'invoice_journal_id' in ui_order.keys():
            result['multi_id'] = ui_order['invoice_journal_id']
        return result

    def _prepare_invoice_vals(self):
        self.ensure_one()
        timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
        invoice_date = fields.Datetime.now() if self.session_id.state == 'closed' else self.date_order
        vals = {
            'invoice_origin': self.name,
            'itp_ncf_origen': self.refunded_order_ids.account_move.name,
            'itp_rnc_origen': self.refunded_order_ids.account_move.itp_vat_factura,
            'journal_id': self.multi_id.id or self.session_id.config_id.invoice_journal_id[0].id,
            'move_type': 'out_invoice' if self.amount_total >= 0 else 'out_refund',
            'ref': self.name,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self._get_partner_bank_id(),
            # considering partner's sale pricelist's currency
            'currency_id': self.pricelist_id.currency_id.id,
            'invoice_user_id': self.user_id.id,
            'invoice_date': invoice_date.astimezone(timezone).date(),
            'fiscal_position_id': self.fiscal_position_id.id,
            'invoice_line_ids': self._prepare_invoice_lines(),
            'invoice_payment_term_id': self.partner_id.property_payment_term_id.id or False,
            'invoice_cash_rounding_id': self.config_id.rounding_method.id
            if self.config_id.cash_rounding and (not self.config_id.only_round_cash_method or any(p.payment_method_id.is_cash_count for p in self.payment_ids))
            else False
        }
        if self.note:
            vals.update({'narration': self.note})
        return vals


    @api.model
    def _process_order(self, order, draft, existing_order):
        if 'invoice_journal_id' in order.keys():
          order['data']['invoice_journal_id'] = order['invoice_journal_id']
        new = super(Superforjournalid,self)._process_order(order, draft, existing_order)
        return new