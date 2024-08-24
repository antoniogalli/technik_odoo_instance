# -*- coding: utf-8 -*-


from odoo import fields, models, api, tools, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def  get_fechaformateada(self,fecha):
        if not fecha:
            return " "
        return fecha.strftime('%d/%m/%y')

