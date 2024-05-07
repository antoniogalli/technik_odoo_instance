# -*- coding: utf-8 -*-
# from odoo import http


# class LinSetDeliveryAddress(http.Controller):
#     @http.route('/lin_set_delivery_address/lin_set_delivery_address/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lin_set_delivery_address/lin_set_delivery_address/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lin_set_delivery_address.listing', {
#             'root': '/lin_set_delivery_address/lin_set_delivery_address',
#             'objects': http.request.env['lin_set_delivery_address.lin_set_delivery_address'].search([]),
#         })

#     @http.route('/lin_set_delivery_address/lin_set_delivery_address/objects/<model("lin_set_delivery_address.lin_set_delivery_address"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lin_set_delivery_address.object', {
#             'object': obj
#         })
