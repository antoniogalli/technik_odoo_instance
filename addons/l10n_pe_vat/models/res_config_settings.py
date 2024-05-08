from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    token_for_api = fields.Char(
        string="Token for API",
        help="The token to use when consult API.",
        related="company_id.L10n_pe_vat_token_api",
        readonly=False,
        # groups="L10N_PE_VAT",
    )

    def action_change_token(self):
        return self.company_id.action_change_token()
