from odoo import models, fields, api
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    L10n_pe_vat_token_api = fields.Char(
        string="Token for API",
        ondelete="restrict",
        help="To change the token to do api search",
    )

    def get_apis_net_pe_token(self):
        self.ensure_one()

        return self.L10n_pe_vat_token_api

    def apis_dni_url(self, dni):
        return f"https://api.apis.net.pe/v1/dni?numero={dni}"

    def apis_ruc_url(self, ruc):
        return f"https://api.apis.net.pe/v1/ruc?numero={ruc}"
