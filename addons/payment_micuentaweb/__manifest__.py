# coding: utf-8
#
# Copyright © Lyra Network.
# This file is part of Mi Cuenta Web plugin for Odoo. See COPYING.md for license details.
#
# Author:    Lyra Network (https://www.lyra.com)
# Copyright: Copyright © Lyra Network
# License:   http://www.gnu.org/licenses/agpl.html GNU Affero General Public License (AGPL v3)

{
    'name': 'Mi Cuenta Web Payment Acquirer',
    'version': '1.2.4',
    'summary': 'Accept payments with Mi Cuenta Web secure payment gateway.',
    'category': 'Accounting',
    'author': 'Lyra Network',
    'website': 'https://www.lyra.com/',
    'license': 'AGPL-3',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_micuentaweb_templates.xml',
        'data/payment_acquirer_data.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
}
