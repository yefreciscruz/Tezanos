# -*- coding: utf-8 -*-
# from odoo import http


# class ItpContaDominicana(http.Controller):
#     @http.route('/itp_conta_dominicana/itp_conta_dominicana', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/itp_conta_dominicana/itp_conta_dominicana/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('itp_conta_dominicana.listing', {
#             'root': '/itp_conta_dominicana/itp_conta_dominicana',
#             'objects': http.request.env['itp_conta_dominicana.itp_conta_dominicana'].search([]),
#         })

#     @http.route('/itp_conta_dominicana/itp_conta_dominicana/objects/<model("itp_conta_dominicana.itp_conta_dominicana"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('itp_conta_dominicana.object', {
#             'object': obj
#         })
