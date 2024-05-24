# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    inventory_show_signature = fields.Boolean(
        "Show digital sign in Inventory ?")
    inventory_sign_confirm = fields.Boolean("Check sign before Confirmation")
    inventory_sign_options = fields.Selection([('picking', 'Picking Operations'), (
        'delivery', 'Delivery Slip'), ('both', 'Both')], string="Sign applicable inside")
    inventory_enable_other_sign_option = fields.Boolean(
        "Enable Other Sign Option")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_show_signature = fields.Boolean(
        "Show digital sign in Inventory ?", related="company_id.inventory_show_signature", readonly=False)
    inventory_sign_confirm = fields.Boolean(
        "Check sign before Confirmation", related="company_id.inventory_sign_confirm", readonly=False)
    inventory_sign_options = fields.Selection([('picking', 'Picking Operations'), ('delivery', 'Delivery Slip'), (
        'both', 'Both')], default='both', related="company_id.inventory_sign_options", string="Sign applicable inside", readonly=False)
    inventory_enable_other_sign_option = fields.Boolean(
        "Enable Other Sign Option", related="company_id.inventory_enable_other_sign_option", readonly=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    digital_sign = fields.Binary("Signature")
    inventory_show_signature = fields.Boolean(
        string="Show digital sign in Inventory ?", related="company_id.inventory_show_signature")
    inventory_sign_confirm = fields.Boolean(
        "Check sign before Confirmation", related="company_id.inventory_sign_confirm")
    inventory_sign_options = fields.Selection([('picking', 'Picking Operations'), ('delivery', 'Delivery Slip'), (
        'both', 'Both')], related="company_id.inventory_sign_options", string="Sign applicable inside")

    inventory_show_enable_other_sign = fields.Boolean(
        "Enable Other sign Option", related="company_id.inventory_enable_other_sign_option")
    sign_by = fields.Char("Signed By")
    designation = fields.Char("Designation")
    sign_on = fields.Datetime(
        'Sign on', default=lambda self: fields.Datetime.now())

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.inventory_sign_confirm:
            if not self.digital_sign:
                raise UserError(_('There is no Signature'))
        return res
