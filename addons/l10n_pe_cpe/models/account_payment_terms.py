# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    sunat_payment_type = fields.Selection(
        [("Contado", "Contado"), ("Credito", "Crédito")],
        string="Tipo de pago SUNAT",
        default="Contado",
    )
