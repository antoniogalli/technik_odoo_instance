# -*- coding: utf-8 -*-
{
    'name': 'Mail Notification',
    'version': '1.0',
    'category': 'Discuss',
    'summary': 'Chat, mail gateway and private channels',
    'description': "",
    'website': 'https://www.odoo.com/page/discuss',
    'depends': ['base', 'base_setup', 'bus', 'web_tour'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/ir_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': True,  # Esta clave hace que el módulo sea autoinstalable   
     
    'application': True,   
    'license': 'LGPL-3',

}
