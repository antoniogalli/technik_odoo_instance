# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class lin_set_delivery_address(models.Model):
#     _name = 'lin_set_delivery_address.lin_set_delivery_address'
#     _description = 'lin_set_delivery_address.lin_set_delivery_address'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class LinasoftAccountMove(models.Model):
_inherit = 'account.move'


	def create(self, values):
		
		super(LinasoftAccountMove, self).create(values)		
