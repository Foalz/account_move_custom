from odoo import fields, models, api
from odoo.exceptions import UserError

class account_journal_custom (models.Model):
    _inherit = "account.journal"

    def action_create_duplicates(self):
        current_company = self.env.company
        companies = self.env["res.company"].search([])
        account_controls = fields.One2many("account.account")

        #Computing a list of companies different of current company
        rest_of_companies = list(filter(lambda x: x != current_company, [c for c in companies])) 
        for rec in self:
            for company in rest_of_companies:
                raise UserError(self.env["account.account"].with_company(current_company).search([]))
                self.env["account.journal"].with_company(company).sudo().create(
                    {
                        "name": rec.name,
                        "type": rec.type,
                        "code": rec.code,
                    }
                )
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Creacion exitosa',
                'message': '¡El diario contable ha sido duplicado satisfactoriamente!',
                'sticky': False,
                'type': 'success',
                'context': { 
                }
            },
        }
        return action
