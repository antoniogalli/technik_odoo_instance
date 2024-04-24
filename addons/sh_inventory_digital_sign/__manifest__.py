# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Digital Signature in Inventory",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "13.0.1",
    
    "license": "OPL-1",

    "category": "Warehouse",

    "summary": "digital signature Inventory,digital signature stock,digital sign warehouse, Digital Signature pickings, inventory Digital Signature, picking operation Digital Signature Odoo",
    "description": """This module useful to give digital signature features in inventory/picking operations. Digital signature useful for approval, security purpose, contract, etc. If you want to digital sign is compulsory so you can make it just tick 'Check Sign before confirmation' in the configuration setting. After checking this field if you make a inventory/picking operations without a sign so it will give you a warning. We have added a new feature for other sign option so you can add details like sign by, designation, sign date-time, etc. You can print a report with a digital signature and other information.""",

    "depends": ['stock'],

    "data": [
        "views/digital_sign_settings.xml",
        "views/digital_sign.xml",
        "reports/digital_sign_report.xml",
    ],
    "images": ["static/description/background.png", ],

    "installable": True,
    "application": True,
    "auto_install": False,
    "price": "12",
    "currency": "EUR"

}
