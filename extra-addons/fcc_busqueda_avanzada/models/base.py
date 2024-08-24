# -*- coding: utf-8 -*-
import pprint

from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.osv import expression


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        models = self.env['fcc.busqueda.avanzada.config'].search([]).mapped('model')
        if self._name in models:
            fields,type_search = self.get_search_fields(self._name)
            if fields and name:
                zz = [[(field.name, operator, name)] for field in fields]
                args = expression.OR(zz)
                if type_search == "for_words":
                    search_terms = name.split()
                    domain = []
                    for field in fields:
                        yy = [[(field.name, operator, term)] for term in search_terms]
                        argsx = expression.AND(yy)
                        domain.append(argsx)
                    argsforwords = expression.OR(domain)
                    args = argsforwords
                name = ''
        res = super(BaseModel, self).name_search(name, args, operator, limit)
        return res

    def get_search_fields(self, model):
        search_config = self.env['fcc.busqueda.avanzada.config'].search([
            ('model', '=', model)
        ])
        return search_config.field_ids, search_config.type_search
