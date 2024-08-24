# -*- coding: utf-8 -*-

{
    "name": "Reportes",
    "version": "13.0.1.0.2",
    "author": "Antonio",
    "license": "OPL-1",
    "category": "Accounting",
    "website": "https://www.flexxoone",
    "description": """Multiple Invoice Templates ,  
    """,
    "summary": "¡Diversas plantillas de facturas a un solo Clic!",
    "data": [
        "views/templates.xml",
    ],
    "qweb": [
    ],
    "depends": ["sistemerp_ereport_template",'sale','account'],
    "external_dependencies": {"python": ["img2pdf", "fpdf", "num2words"]},
    "images": ["static/description/splash-screen.png"],
    "installable": True,
    "auto_install": False,
    "web_preload": True,
}
