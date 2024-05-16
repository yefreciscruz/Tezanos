# -*- coding: utf-8 -*-
{
    'name': "Contabilidad República Dominicana",

    'summary': """
        Actualización de formatos, vistas y secuencias
        para control de vencimientos y formas de pago""",

    'description': """
        Se debe instalar el módulo y cargar los diarios respectivos
    """,

    'author': "Carlos García - IT Profis",
    'website': "https://www.itprofis-gt.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'point_of_sale', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/report_invoice_document.xml',
        'views/account_journal_form.xml',
        'views/account_invoice_view.xml',
        'views/res_partner_view.xml',
        'views/view_move_tree.xml',
    ],
    #'assets': {
    #    'point_of_sale.assets': [
    #        'itp_conta_dominicana/static/src/xml/pos.xml',
    #        # 'itp_conta_dominicana/static/src/js/pos_order_receipt.js',
    #        'itp_conta_dominicana/static/src/js/pos.js',
    #        'itp_conta_dominicana/static/src/js/payment.js',
    #        ]
    # },

}
