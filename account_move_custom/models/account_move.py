# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import json

class account_move_custom(models.Model):
    _description = 'Custom module to add fields to invoices'
    _inherit = 'account.move'

    invoice_required = fields.Boolean(string="Requiere factura?", default=False)
    is_copy = fields.Boolean(default=False, readonly=1)

    def write(self, vals):
        currency = self.env.ref("base.USD")
        current_company = self.env.company
        companies = self.env["res.company"].search([])
        rest_of_companies = list(filter(lambda x: x != current_company, [c for c in companies])) 
        invoice_lines = []

        if ('invoice_required' in vals) and vals['invoice_required']:
            for invoice in self:
                for company in rest_of_companies:
                    rate_currency = self.env["res.currency"].with_company(company).search([
                        ('name', '=', 'USD'),
                    ], limit=1).rate_ids.search([('name', '=', invoice.invoice_date)]).company_rate
                    journal_id = self.env["account.journal"].with_company(company).search(
                            [("code", "=", invoice.journal_id.code), 
                             ("company_id", "=", company.id)
                            ]).id
                    for invoice_line in invoice.invoice_line_ids:
                        invoice_lines.append({
                            "product_id": invoice_line.product_id,
                            "name": invoice_line.name,
                            "quantity": invoice_line.quantity,
                            "price_unit": invoice_line.price_unit / rate_currency,
                        })
                    self.env["account.move"].with_company(company).sudo().create({
                        "partner_id": invoice.partner_id,
                        "move_type": invoice.move_type,
                        "name": invoice.name,
                        "is_copy": True,
                        "invoice_date": invoice.invoice_date,
                        "invoice_line_ids": invoice_lines,
                        "journal_id": journal_id,
                    }).action_post()
        res = super(account_move_custom, self).write(vals)
        return res

    def get_new_journal(self, journal_id):
        """
            This function has a dictionary of current registered journals ids, categorized
            by currency in a tuple: (first_curr, second_curr)

            In this case, lets take the following example:

            {
                "airlines": (84, 70),
                "third_parties": (34, 41),
                "hotels": (20, 90),
                "own": (14, 30),
                "suppliers": (25, 50)
            }
            
            and let journal_id = 84

            The first loop returns a tuple, where we are checking if journal_id is inside that tuple.
            In this case, yes, 84 is in the tuple, and, is at first position, which means that is a 
            'first_curr' journal id.

            Then, the following instruction:
            if journal_id in journal: 
                return list(filter(lambda id: id != journal_id, journal))[0]

            is taking the tuple (84, 70), and building a new list, with the other id:

            [70] --> This is the result of list(filter(lambda id: id != journal_id, journal))
            and then, we return the only element of that list, which is 70.
        """
        user = self.env.user 
        agency_id = self.env['agencias.agencias'].search([('user_ids','=',user.id)],limit=1)
        journals = {
            "airlines": (agency_id.FPA_aerolinea.id, agency_id.FPA_aerolinea_USD.id),
            "third_parties": (agency_id.FPCT_cliente.id, agency_id.FPCT_cliente_USD.id),
            "hotels": (agency_id.FPH_hotel.id, agency_id.FPH_hotel_USD.id),
            "own": (agency_id.FP_cliente.id, agency_id.FP_cliente_USD.id),
            "suppliers": (agency_id.FP_proveedores.id, agency_id.FP_proveedores_USD.id)
        }
        
        for journal in journals.values():
            if journal_id in journal: 
                return list(filter(lambda id: id != journal_id, journal))[0]

