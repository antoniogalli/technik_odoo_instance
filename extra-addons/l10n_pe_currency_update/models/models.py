# -*- coding: utf-8 -*-
import pprint

import requests
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    tipotasa = fields.Selection([('compra', 'Tasa de compra'),
                                 ('venta', 'Tasa de venta')], string='Tasa de Cambio',default='compra')

class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    def token(self):
        user = self.env.user
        company = self.env.user.company_id
        if len(company) == 0:
            raise UserError("the user dont have asociated company.")

        token = self.env.user.company_id.L10n_pe_vat_token_api

        return token

    @api.model
    def actualizardolaressunat(self):

        API_DOLAR="""https://api.apis.net.pe/v1/tipo-cambio-sunat"""
        try:
            response = requests.get(
                API_DOLAR.format(),
                timeout=300,
                headers={"Authorization": f"Bearer {self.token()}"},
            )
        except requests.RequestException:
            reponse = False
        print("!" * 80, response)
        if response and response.status_code != 200:
            vals = {"detail": "Not found."}
        else:
            vals = response and response.json() or {"detail": "Not found."}
            currency=self.env['res.currency'].search([('name','=','USD')],limit=1)
            currency_rate = self.env['res.currency.rate'].search([('name', '=', vals['fecha'])], limit=1)
            if currency.tipotasa == 'compra':
                rate = 1 / vals['compra']
            elif currency.tipotasa == 'venta':
                rate = 1 / vals['venta']

            if currency and not currency_rate:
                val = {'currency_id': currency.id, 'rate': rate}
                currency_rate.create(val)
            elif currency and currency_rate:
                val = {'currency_id': currency.id, 'rate': rate}
                currency_rate.write(val)

