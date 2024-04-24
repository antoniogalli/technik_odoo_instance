# -*- coding: utf-8 -*-
{
    "name": "Accounting reports for Peru",
    "category": "Accounting",
    "author": "",
    "summary": "Accounting reports for Peru",
    "version": "1.0",
    "description": """
        Accounting report for sales/purchases
        """,
    "depends": ["sale_management", "account"],
    "data": [
        "data/data.xml",
        "wizard/sale_order_summary_wizard.xml",
        "wizard/account_move_summary_wizard.xml",
        "report/sale_summary.xml",
        "report/account_move_summary_report.xml",
    ],
    "installable": True,
}
