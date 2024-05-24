# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

import json


class AccountMoveSaleSummaryReportWizard(models.TransientModel):
    _name = "account.sale.summary.report.wizard"

    date_start = fields.Date(
        string="Fecha Inicio", required=True, default=fields.Date.today
    )
    date_end = fields.Date(string="Fecha Fin", required=True, default=fields.Date.today)
    report_type = fields.Selection(
        string="Tipo Reporte",
        selection=[("purchases", "Compras"), ("sales", "Ventas")],
        default="sales",
    )

    def get_report(self):
        data = {
            "model": self._name,
            "ids": self.ids,
            "form": {
                "date_start": self.date_start,
                "date_end": self.date_end,
                "report_type": self.report_type,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref(
            "tk_account_reports_pe.account_move_sale_summary_report"
        ).report_action(self, data=data)


class ReportAccountSaleSummaryReportView(models.AbstractModel):
    """
    Abstract Model specially for report template.
    _name = Use prefix `report.` along with `module_name.report_name`
    """

    _name = "report.tk_account_reports_pe.account_sale_summary_report_view"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data["form"]["date_start"]
        date_end = data["form"]["date_end"]
        report_type = data["form"]["report_type"]

        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        invoice_type = ""
        if report_type == "sales":
            invoice_type = "out_invoice"
            report_title = "Reporte de Facturas de Ventas"
        else:
            invoice_type = "in_invoice"
            report_title = "Reporte de Facturas de Compras"

        INVOICES = self.env["account.move"].search(
            [
                ("type", "=", invoice_type),
                ("state", "=", "posted"),
                ("invoice_date", ">=", start_date.strftime(DATETIME_FORMAT)),
                ("invoice_date", "<=", end_date.strftime(DATETIME_FORMAT)),
            ]
        )

        return {
            "doc_ids": data["ids"],
            "doc_model": data["model"],
            "date_start": date_start,
            "date_end": date_end,
            "report_title": report_title,
            "docs": INVOICES,
            "company_id": self.env.company,
        }


class AccountMoveDebtSummaryReportWizard(models.TransientModel):
    _name = "account.debt.summary.report.wizard"

    date_start = fields.Date(
        string="Fecha Inicio", required=True, default=fields.Date.today
    )
    date_end = fields.Date(string="Fecha Fin", required=True, default=fields.Date.today)

    def get_report(self):
        data = {
            "model": self._name,
            "ids": self.ids,
            "form": {
                "date_start": self.date_start,
                "date_end": self.date_end,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref(
            "tk_account_reports_pe.account_move_debt_summary_report"
        ).report_action(self, data=data)


class ReportAccountDebtsSummaryReportView(models.AbstractModel):
    """
    Abstract Model specially for report template.
    _name = Use prefix `report.` along with `module_name.report_name`
    """

    _name = "report.tk_account_reports_pe.account_debt_summary_report_view"

    def get_document_type(self, invoice):
        value = ""
        if invoice:
            if invoice.journal_id:
                if invoice.journal_id.pe_invoice_code:
                    if invoice.journal_id.pe_invoice_code == "00":
                        value = "Otros"
                    elif invoice.journal_id.pe_invoice_code == "01":
                        value = "Factura"
                    elif invoice.journal_id.pe_invoice_code == "02":
                        value = "Recibo por Honorarios"
                    elif invoice.journal_id.pe_invoice_code == "03":
                        value = "Boleta de Ventas"
                else:
                    value = "Factura"
        return value

    def get_vat_type(self, invoice):
        value = ""
        if invoice:
            if invoice.partner_id.vat:
                if invoice.journal_id:
                    if invoice.journal_id.pe_invoice_code:
                        if invoice.journal_id.pe_invoice_code != "03":
                            vat_type_val = invoice.partner_id.vat[0:2]
                            if vat_type_val in ["10", "15"]:
                                value = "Personal"
                            elif vat_type_val == "20":
                                value = "Empresa"
                        else:
                            value = "DNI"
        return value

    def get_payments(self, invoice):
        values = []
        if invoice:
            if invoice.invoice_payment_ref == invoice.name:
                if invoice.invoice_payments_widget != "false":
                    payments = json.loads(invoice.invoice_payments_widget)
                    values = payments["content"]
            else:
                order = self.env["pos.order"].search(
                    [("name", "=", invoice.invoice_payment_ref)]
                )
                payments = []
                for payment in order.payment_ids:
                    payments.append(
                        {
                            "name": "Pago de cliente: " + payment.pos_order_id.name,
                            "journal_name": payment.payment_method_id.name,
                            "amount": payment.amount,
                            "date": payment.payment_date,
                            "ref": order.pos_reference,
                        }
                    )
        return values

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data["form"]["date_start"]
        date_end = data["form"]["date_end"]

        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        INVOICES = self.env["account.move"].search(
            [
                ("type", "in", ["in_invoice", "out_invoice"]),
                ("state", "=", "posted"),
                ("invoice_date", ">=", start_date.strftime(DATETIME_FORMAT)),
                ("invoice_date", "<=", end_date.strftime(DATETIME_FORMAT)),
            ]
        )

        docs = []

        for invoice in INVOICES:
            docs.append(
                {
                    "invoice_date": invoice.invoice_date,
                    "invoice_date_due": invoice.invoice_date_due,
                    "document_type": self.get_document_type(invoice),
                    "serie": invoice.journal_id.code,
                    "number": invoice.internal_number.split("-")[1],
                    "vat_type": self.get_vat_type(invoice),
                    "partner_id": invoice.partner_id,
                    "currency_id": invoice.currency_id,
                    "amount_total": invoice.amount_total,
                    "invoice_payment_state": invoice.invoice_payment_state,
                    "invoice_payments": self.get_payments(invoice),
                    "invoice_residual": invoice.amount_residual,
                    "user_id": invoice.user_id,
                }
            )

        return {
            "doc_ids": data["ids"],
            "doc_model": data["model"],
            "date_start": date_start,
            "date_end": date_end,
            "docs": docs,
            "company_id": self.env.company,
        }
