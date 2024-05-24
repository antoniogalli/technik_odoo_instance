# -*- coding: utf-8 -*-
{
    "name": "Kardex report for product(s)",
    "version": "13.0.0.0.1",
    "price": 200.00,
    "currency": "USD",
    "support": "elio.linarez@tk-peru.com",
    "category": "Reporting",
    "summary": "Kardex Report in Excel/Pdf Format",
    "author": "Elio Linarez TK PEru Team <elio.linarez@tk-peru.com>",
    "depends": ["base", "stock", "stock_account", "account", "tk_account_reports_pe"],
    "images": ["static/description/main_screenshot.png"],
    "data": [
        "kardex.xml",
        "kardex_report.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
    "license": "OPL-1",
}
