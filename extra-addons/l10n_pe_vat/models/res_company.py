from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    L10n_pe_vat_token_api = fields.Char(
        string="Token for API",
        ondelete="restrict",
        help="To change the token to do api search",
    )
