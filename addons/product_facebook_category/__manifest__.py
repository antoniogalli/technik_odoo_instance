# -*- coding: utf-8 -*-

# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Facebook Product Category',
    'version': '13.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'LGPL-3',
    'summary': 'Facebook Product Categories in your products',
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://garazd.biz/r/5zP',
    'description': """
Assigning Facebook product categories to your Odoo products
    """,
    'depends': [
        'website_sale',
        'base_import_helper',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_facebook_category_views.xml',
        'wizard/base_import_helper_views.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
