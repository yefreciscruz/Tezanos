# -*- coding: utf-8 -*-

import time
from odoo import api, models, _


class ReportJournalAudit(models.AbstractModel):
    _name = 'report.bi_pos_multiple_invoice_journal.report_journal_audit'
    _description = 'Journal Report'

    def datalines(self, target_move, journal_ids, sort_selection, data):
        if isinstance(journal_ids, int):
            journal_ids = [journal_ids]
        new_state = ['draft', 'posted']
        tables, where_clause, where_params = self.env['account.move.line']._where_calc([
            ('parent_state', '=', 'posted'),
            ('company_id', '=', self.env.company.id)
        ]).get_sql()
        if target_move == 'posted':
            new_state = ['posted']
        if not data['form'].get('used_context', {})['strict_range']:

            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and not data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        rec = [tuple(new_state), tuple(journal_ids)] + fetch_data[2]
        sql_query = 'SELECT "account_move_line".id FROM ' + fetch_data[0] + \
        ', account_move move, account_account account WHERE "account_move_line".account_id = account.id AND "account_move_line".move_id=move.id AND move.state IN %s AND "account_move_line".journal_id IN %s AND ' + \
                fetch_data[1] + ' ORDER BY '
        if sort_selection == 'date':
            sql_query += '"account_move_line".date'
        else:
            sql_query += 'move.name'
        sql_query += ', "account_move_line".move_id, account.code'
        record_id=[]
        self.env.cr.execute(sql_query, tuple(rec))
        for x in self.env.cr.fetchall():
            record_id.append(x[0])
        return self.env['account.move.line'].browse(record_id)

    def _total_debit(self, data, journal_id):
        new_state = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            new_state = ['posted']
        if not data['form'].get('used_context', {})['strict_range']:

            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and not data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        rec = [tuple(new_state), tuple(journal_id.ids)] + fetch_data[2]
        self.env.cr.execute('SELECT SUM(debit) FROM ' + fetch_data[0] + ', account_move move '
                 'WHERE "account_move_line".move_id=move.id AND move.state IN %s AND "account_move_line".journal_id IN %s AND ' + fetch_data[1] + ' ',tuple(rec))
        return self.env.cr.fetchone()[0] or 0.0

    def _total_credit(self, data, journal_id):
        new_state = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            new_state = ['posted']

        if not data['form'].get('used_context', {})['strict_range']:

            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and not data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        rec = [tuple(new_state), tuple(journal_id.ids)] + fetch_data[2]
        self.env.cr.execute('SELECT SUM(credit) FROM ' + fetch_data[0] + ', account_move move '
                 'WHERE "account_move_line".move_id=move.id AND move.state IN %s AND "account_move_line".journal_id IN %s AND ' + fetch_data[1] + ' ',tuple(rec))
        return self.env.cr.fetchone()[0] or 0.0

    def _total_taxes(self, data, journal_id):
        new_state = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            new_state = ['posted']

        if not data['form'].get('used_context', {})['strict_range']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and not data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        elif data['form'].get('used_context', {})['strict_range'] and data['form'].get('used_context', {})['date_to']:
            if data['form'].get('used_context', {})['strict_range'] == 'posted':
                fetch_data = self.env['account.move.line']._where_calc([
                ('parent_state', '=', data['form'].get('used_context', {})['state']),
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
            else:
                fetch_data = self.env['account.move.line']._where_calc([
                ('journal_id', 'in', data['form'].get('used_context', {})['journal_ids']),
                
                ('company_id', '=', self.env.company.id)]).get_sql()
        rec = [tuple(new_state), tuple(journal_id.ids)] + fetch_data[2]
        sql_query = """
            SELECT rel.account_tax_id, SUM("account_move_line".balance) AS base_amount
            FROM account_move_line_account_tax_rel rel, """ + fetch_data[0] + """ 
            LEFT JOIN account_move move ON "account_move_line".move_id = move.id
            WHERE "account_move_line".id = rel.account_move_line_id
                AND move.state IN %s
                AND "account_move_line".journal_id IN %s
                AND """ + fetch_data[1] + """
           GROUP BY rel.account_tax_id"""
        self.env.cr.execute(sql_query, tuple(rec))
        record_id = []
        base_amounts = {}
        for x in self.env.cr.fetchall():
            record_id.append(x[0])
            base_amounts[x[0]] = x[1]

        res = {}
        for tax in self.env['account.tax'].browse(record_id):
            self.env.cr.execute(
                'SELECT sum(debit - credit) FROM ' + fetch_data[0] + ', account_move move '
                         'WHERE "account_move_line".move_id=move.id AND move.state IN %s AND "account_move_line".journal_id IN %s AND ' + fetch_data[1] + ' AND tax_line_id = %s',tuple(rec + [tax.id]))
            res[tax] = {
                'base_amount': base_amounts[tax.id],
                'tax_amount': self.env.cr.fetchone()[0] or 0.0,
            }
            if journal_id.type == 'sale':
                res[tax]['base_amount'] = res[tax]['base_amount'] * -1
                res[tax]['tax_amount'] = res[tax]['tax_amount'] * -1
        return res

    @api.model
    def _get_report_values(self, docids, data=None):

        target_move = data['form'].get('target_move', 'all')
        sort_selection = data['form'].get('sort_selection', 'date')
        res = {}
        for journal in data['form']['journal_ids']:
            res[journal] = self.with_context(data['form'].get('used_context', {})).datalines(target_move,journal,sort_selection,data)
        return {
            'doc_ids': data['form']['journal_ids'],
            'doc_model': self.env['account.journal'],
            'data': data,
            'docs': self.env['account.journal'].browse(
                data['form']['journal_ids']),
            'time': time,
            'datalines': res,
            'total_credit': self._total_credit,
            'total_debit': self._total_debit,
            'total_taxes': self._total_taxes,
        }