# -*- coding: utf-8 -*-
# from odoo import http


# class SitAjustesVarios(http.Controller):
#     @http.route('/sit_ajustes_varios/sit_ajustes_varios/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sit_ajustes_varios/sit_ajustes_varios/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sit_ajustes_varios.listing', {
#             'root': '/sit_ajustes_varios/sit_ajustes_varios',
#             'objects': http.request.env['sit_ajustes_varios.sit_ajustes_varios'].search([]),
#         })

#     @http.route('/sit_ajustes_varios/sit_ajustes_varios/objects/<model("sit_ajustes_varios.sit_ajustes_varios"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sit_ajustes_varios.object', {
#             'object': obj
#         })
