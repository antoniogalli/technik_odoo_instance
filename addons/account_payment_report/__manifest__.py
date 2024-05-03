# -*- coding: utf-8 -*-
{
    'name': "account_payment_report",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Odoo",
    'website': "http://www.odoo.com",
    'category': 'Uncategorized',
    'version': '13.0.0.1',
    'depends': ['account','sales_team'],
    'data': [
        'views/report_account_payment.xml',
        'views/report_account_payment_view.xml',
        'wizard/account_payment_report_wizard_view.xml'
    ],
}