# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError

class payslip_custom (models.Model):
    _inherit = "hr.payslip.line"

    additions = fields.Float(
        string="Aportes",
        readonly=True,
        default=0,
        compute="_compute_addition"
    )
    substractions = fields.Float(
        string="Deducciones",
        default=0,
        readonly=True,
        compute="_compute_substraction"
    )

    @api.model
    def _compute_addition(self):
        for rec in self:
            code = rec.category_id.code
            rec.additions = rec.total if code == "BON" else 0

    @api.model
    def _compute_substraction(self):
        for rec in self:
            code = rec.category_id.code
            rec.substractions = rec.total if code == "DED" or code == "PREST" else 0


