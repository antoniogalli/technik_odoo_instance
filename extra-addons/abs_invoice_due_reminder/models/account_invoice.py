# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _
from datetime import date
 

class AccountMove(models.Model):
    _inherit = "account.move"

    due_reminder_date = fields.Date()

    @api.model
    def send_email_from_customer(self):
        today_date = date.today()
        today_date = str(today_date)
        obj = self.env['account.move'].search([('invoice_payment_state','!=',('paid')),('state','!=',('draft'))])
        if obj:
            context = self._context
            current_uid = context.get('uid')
            current_login_user = self.env['res.users'].browse(current_uid)
            for invoice in obj:
                email_to = []
                obj_date = str(invoice.due_reminder_date)
                if invoice and obj_date == today_date:
                    email_to.append(invoice.partner_id)
                    
                    template1 = self.env.ref('abs_invoice_due_reminder.email_template_edi_invoices')
                    if template1:
                        mail_create = template1.send_mail(invoice.id)
                        if mail_create:
                            mail = self.env['mail.mail'].browse(mail_create).send()

