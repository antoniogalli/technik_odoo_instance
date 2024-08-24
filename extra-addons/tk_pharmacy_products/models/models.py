# -*- coding: utf-8 -*-
import pprint

from odoo import models, fields, api

class TkDosage(models.Model):
    _name = "tk.dosage"
    _description = "Dosage (box, pack, etc)"
    name = fields.Char(
        string = "Dosage")

class TkPharmacyRoute(models.Model):
    _name = "tk.route"
    _description = "Administration route (oral, intravenous, etc)"
    name = fields.Char(
        string = "Route")

class TkPharmacyForm(models.Model):
    _name = "tk.pharmaceutical_form"
    _description = "Pharmaceutical form (powder, tablet, etc)"
    name = fields.Char(
        string = "Pharmaceutical form")

class TKPharmacyProduct(models.Model):
    _inherit = "product.template"
    
    Health_register = fields.Char(
        string = "Health register")

    pharmaceutical_composition = fields.Char(
        string = "Pharmaceutical composition")

    pharmaceutical_form = fields.Many2one("tk.pharmaceutical_form",
        string = "Pharmaceutical form")

    route = fields.Many2one("tk.route",
        string = "Route")
        
    dosage = fields.Many2one("tk.dosage", 
        string='Dosage') 

    quantity_per_presentation = fields.Integer(
        string = "Quantity per presentation",)

    origin = fields.Many2one("res.country",
        string = "Origin")

    batch = fields.Char(
        string = "Batch")

    due_date = fields.Date(
        string = "Due date")

    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     if not args:
    #         args = []
    #
    #     # Dividir la cadena de búsqueda en palabras
    #     search_terms = name.split()
    #
    #     domain = []
    #     for term in search_terms:
    #         # Crear un dominio que busca registros donde el campo "name" o "code" contenga la palabra actual
    #         domain += ['|','|','|', ('name', operator, term), ('default_code', operator, term),('pharmaceutical_composition', operator, term),('batch', operator, term)]
    #     pprint.pprint(domain)
    #
    #     records = self.search(domain + args, limit=limit)
    #     return records.name_get()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    Health_register = fields.Char(
        string="Health register",related="product_id.Health_register")

    pharmaceutical_composition = fields.Char(
        string="Pharmaceutical composition",related="product_id.pharmaceutical_composition")

    pharmaceutical_form = fields.Many2one("tk.pharmaceutical_form",
                                          string="Pharmaceutical form"
                                          ,related="product_id.pharmaceutical_form")

    route = fields.Many2one("tk.route",
                            string="Route",related="product_id.route")

    dosage = fields.Many2one("tk.dosage",
                             string='Dosage',related="product_id.dosage")

    quantity_per_presentation = fields.Integer(
        string="Quantity per presentation",related="product_id.quantity_per_presentation" )

    origin = fields.Many2one("res.country",
                             string="Origin",related="product_id.origin")

    batch = fields.Char(
        string="Batch",related="product_id.batch")

    due_date = fields.Date(
        string="Due date",related="product_id.due_date")

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    Health_register = fields.Char(
        string="Health register",related="product_id.Health_register")

    pharmaceutical_composition = fields.Char(
        string="Pharmaceutical composition",related="product_id.pharmaceutical_composition")

    pharmaceutical_form = fields.Many2one("tk.pharmaceutical_form",
                                          string="Pharmaceutical form"
                                          ,related="product_id.pharmaceutical_form")

    route = fields.Many2one("tk.route",
                            string="Route",related="product_id.route")

    dosage = fields.Many2one("tk.dosage",
                             string='Dosage',related="product_id.dosage")

    quantity_per_presentation = fields.Integer(
        string="Quantity per presentation",related="product_id.quantity_per_presentation" )

    origin = fields.Many2one("res.country",
                             string="Origin",related="product_id.origin")

    batch = fields.Char(
        string="Batch",related="product_id.batch")

    due_date = fields.Date(
        string="Due date",related="product_id.due_date")