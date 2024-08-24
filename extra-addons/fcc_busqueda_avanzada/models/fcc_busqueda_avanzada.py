# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger()


class EasySearchConfig(models.Model):
    _name = 'fcc.busqueda.avanzada.config'
    _rec_name = 'model_id'
    _description = 'Configuración de Búsqueda Avanzada'

    model_id = fields.Many2one(comodel_name="ir.model", string="Nombre del Modelo", required=True, )
    model = fields.Char(string="Modelo", related="model_id.model", store=True)
    type_search=fields.Selection([('simple','Simple'),('for_words','Por Palabras')],string="Tipo de Búsqueda",default="simple")
    field_ids = fields.Many2many(
        "ir.model.fields",
        "easy_id",
        "field_id",
        "fcc_busqueda_avanzada_fields_ref",
        string="Campos para ser utilizados en la búsqueda",
        required=True,
    )
    all_field_ids = fields.Many2many(
        "ir.model.fields",
        "easy1_id",
        "field2_id",
        "fcc_busqueda_avanzada_all_fields_ref",
        string="Todos los Campos",
        compute="calc_all_fields",
        store=True
    )

    @api.depends('model_id', 'model_id.field_id')
    def calc_all_fields(self):
        for rec in self:
            rec.all_field_ids = rec.model_id.field_id.ids
