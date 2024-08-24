# -*- coding: utf-8 -*-
{
    'name': "TechniK Pharmacy Product fields",

    'summary': """
        Add  custom fields to `product.template`""",

    'description': """
    This module adds custom fields to the product template form in Odoo.
    This allows you to add additional information to your products, concerning the pharmacy.""",

    'author': "p.p Linarez",
    'website': "--",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
