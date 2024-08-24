# -*- coding: utf-8 -*-
# from odoo import http


# class TkPharmacyProducts(http.Controller):
#     @http.route('/tk_pharmacy_products/tk_pharmacy_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tk_pharmacy_products/tk_pharmacy_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tk_pharmacy_products.listing', {
#             'root': '/tk_pharmacy_products/tk_pharmacy_products',
#             'objects': http.request.env['tk_pharmacy_products.tk_pharmacy_products'].search([]),
#         })

#     @http.route('/tk_pharmacy_products/tk_pharmacy_products/objects/<model("tk_pharmacy_products.tk_pharmacy_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tk_pharmacy_products.object', {
#             'object': obj
#         })
