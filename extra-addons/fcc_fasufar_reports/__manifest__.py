# -*- coding: utf-8 -*-
{
    'name': "fcc_fasufar_reports",

    'summary': """
       PRepara los reportes para emitirlos en el formato de fasufar
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Fabian Calderon Cadena",
    'website': "http://www.odoosoluciones.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'tk_pharmacy_products', 'purchase', 'l10n_pe_cpe', 'l10n_pe_eguide'],

    # always loaded
    'data': [

        'views/views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/account_move_views.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_journal_view.xml',
         'views/stock_move_views.xml',

        'report/cotizacion.xml',
        'report/ordencompra.xml',
        'report/account_move_invoice.xml',
        'report/account_move_out_refund.xml',
        'report/guia_remision.xml',
        'report/letra_cambio_apromed.xml',
        'views/pos_fasufar.xml',
        'views/templates.xml',

    ],
    'images': ['static/description/icon.png'],
    "installable": True,
    "auto_install": False,
    'qweb': ['static/src/xml/pos.xml'],
    'demo': [
        'demo/demo.xml',
    ],
}
