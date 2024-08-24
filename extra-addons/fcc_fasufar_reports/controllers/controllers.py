# -*- coding: utf-8 -*-
# from odoo import http


# class FccFasufarReports(http.Controller):
#     @http.route('/fcc_fasufar_reports/fcc_fasufar_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fcc_fasufar_reports/fcc_fasufar_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fcc_fasufar_reports.listing', {
#             'root': '/fcc_fasufar_reports/fcc_fasufar_reports',
#             'objects': http.request.env['fcc_fasufar_reports.fcc_fasufar_reports'].search([]),
#         })

#     @http.route('/fcc_fasufar_reports/fcc_fasufar_reports/objects/<model("fcc_fasufar_reports.fcc_fasufar_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fcc_fasufar_reports.object', {
#             'object': obj
#         })
