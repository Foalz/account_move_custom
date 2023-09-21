from odoo import fields, models, api
import random
from odoo.exceptions import UserError

class account_journal_custom (models.Model):
    _inherit = "account.journal"

    def action_create_duplicates(self):
        current_user = self.env.user
        current_company = self.env.company
        companies = self.env["res.users"].search([("id", "=", current_user.id)]).company_ids
        account_control_current_company = self.env["account.account"].search([("company_id", "=", current_company.id)])

        #Computing a list of companies different of current company
        rest_of_companies = list(filter(lambda x: x != current_company, [c for c in companies])) 
        acc_lst = []
        for rec in self:
            for company in rest_of_companies:
                # for acc in account_control_current_company:
                    # acc_lst.append({
                        # "code": ,
                        # "name": acc.name,
                        # "user_type_id": acc.user_type_id.id,
                        # "reconcile": acc.reconcile,
                        # "currency_id": acc.currency_id.id,
                        # "company_id": company.id
                    # })  

                # self.env["account.account"].with_company(company).sudo().search([("company_id", "=", company.id)]).create(acc_lst)
                self.env["account.journal"].with_company(company).sudo().create(self.get_all_fields(rec, company))

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

    def get_all_fields(self, rec, company):
        """
            VARIABLES
                rec: is a class that stores the current record that odoo is 
                catching, where _fields is the attribute of that class which 
                stores all the values of the record.

            PROCEDURE
                with type(rec) we are getting the class, and with attribute __dict__
                we are getting a dictionary with its methods, attributes, constructors...

                We do not need all those things, we only just need the '_fields' attribute.
                So, with the following loop:

                for field in type(rec).__dict__['_fields'].keys():
                ... #Code
                
                We are getting in variable 'field', the name of the field that is on the record.
                
                To avoid errors, we created a list 'fields_to_be_copied', which stores all field names
                that we want to copy.

                The following lines:
                    try:
                        new_rec[field] = rec[field].id
                    except:
                        new_rec[field] = rec[field]

                It is trying to get attribute 'id' of that field (case for many2one fields), if that field 
                is not a many2one field, throws an error and go to except and it assumes that is another type
                of data.
        """
        # Select the fields you want to copy to avoid errors
        fields_to_be_copied = [
            "name", "code", "type", "refund_sequence", "currency_id",
            "company_id", "mail_template_id", "type_control_ids", "account_control_ids"
        ]
        new_rec = {}
        for field in type(rec).__dict__['_fields'].keys():
            if field in fields_to_be_copied:
                try:
                    new_rec[field] = rec[field].id
                except:
                    new_rec[field] = rec[field]
        new_rec['company_id'] = company.id
        return new_rec
