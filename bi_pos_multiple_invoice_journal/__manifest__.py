# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "Multiple Invoice Journal Selection on POS",
	"version" : "16.0.0.0",
	"category" : "Point of Sale",
	'summary': 'POS multi journal selection pos multi invoice journal pos multiple journal selection pos multiple invoice journal selection from pos journal pos select invoice journal point of sale multi journal point of sale multi invoice journal pos set invoice journal',
	"description": """
		POS Multi Invoices Journal in odoo,
		Configure invoice journal from POS in odoo,
		Multi Invoice Journal in odoo,
		Print multi invoice journal report in odoo,
		POS Journal Entry wizard in odoo, 
	""",
	"author": "BrowseInfo",
	"website" : "https://www.browseinfo.com",
	"price": 35,
	"currency": 'EUR',
	"depends" : ['base','account','point_of_sale'],
	"data": [
		'security/ir.model.access.csv',
		'wizard/journal_wizard.xml',
		'views/pos_config_inherit.xml',
		'report/report.xml',
		'report/report_journal_audit.xml',
	],
	'assets': {
		'point_of_sale.assets': [
			"bi_pos_multiple_invoice_journal/static/src/css/invoice_journal.css",
			"bi_pos_multiple_invoice_journal/static/src/js/invoice_journal.js",
			"bi_pos_multiple_invoice_journal/static/src/js/PaymentScreen.js",
			"bi_pos_multiple_invoice_journal/static/src/js/JournalButton.js",
			'bi_pos_multiple_invoice_journal/static/src/xml/JournalButton.xml',
			'bi_pos_multiple_invoice_journal/static/src/xml/pos_invoice_journal.xml'
		],
	},
	"auto_install": False,
	"installable": True,
	"live_test_url":'https://youtu.be/vdMhAp4dwOo',
	"images":["static/description/Banner.gif"],
	'license': 'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
