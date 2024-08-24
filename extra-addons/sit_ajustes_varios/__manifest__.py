# -*- coding: utf-8 -*-
{
    'name': "SIT ajustes varios",

    'summary': """
        Ajustes varios Apromed
        """,

    'description': """
        Ajustes varios Apromed:
        - 1- habilitar la columna  que dice “End of life date” debe decir “Fecha Vencimiento
        - 2. ajuste de inventario. Observamos que  cuando se usa el scaner de codigo de barras en la captura de los productos no trae el codigo scaneado. (CONCLIENTE)
        - 3. De mas de 100 item solo pasan 17 no muestra paginacion. Deberia permitir la lista
        - 4. En el proceso de ventas se debe agregar una columna contadora de ITEM a la izquierda.

    """,


    "author": "Daniel Jove<daniel.jove@service-it.com.ar>",
    "license": "Other proprietary",
    'website': "https://service-it.com.ar",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    "version": "13.0.1.0.0.20231120.01",

    # any module necessary for this one to work correctly
    'depends': ['base','account','stock','fcc_fasufar_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move_views.xml',
        'views/sale_order.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
