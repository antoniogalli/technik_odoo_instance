# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from pdf417gen.encoding import to_bytes, encode_high, encode_rows
from pdf417gen.util import chunks
from pdf417gen.compaction import compact_bytes
from pdf417gen import render_image
import tempfile
from base64 import encodestring
from odoo.exceptions import UserError
import re
from io import StringIO, BytesIO
try:
    import qrcode
    qr_mod = True
except:
    qr_mod = False


import logging
_logger = logging.getLogger(__name__)



class sit_sale_order(models.Model):
    _inherit = 'sale.order.line'

    line_counter = fields.Integer(string="Line Counter", compute='_compute_line_counter')

    # @api.depends('order_id.order_line')
    # def _compute_line_counter(self):
    #     for line in self:
    #         line.line_counter = len(line.order_id.order_line)

    @api.depends('order_id.order_line')
    def _compute_line_counter(self):
        for index, line in enumerate(self.order_id.order_line):
            line.line_counter = index + 1

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
