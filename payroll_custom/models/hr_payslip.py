# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError

class payroll_custom(models.Model):
    _inherit = "hr.payslip"

    payslip_line_id = fields.One2many(
        "hr.payslip.line",
        "id",
        string="Payslip line",
    )
    total_additions = fields.Float(
        string="Total aportes",
        default=0,
        readonly=True,
        compute="_compute_total_additions"
    )
    total_substractions = fields.Float(
        string="Total deducciones",
        default=0,
        readonly=True,
        compute="_compute_total_substractions"
    )
    total_sum = fields.Float(
        string="Suma total",
        default=0,
        readonly=True,
        compute="_compute_total_sum"
    )

    @api.depends('payslip_line_id')
    def _compute_total_additions(self):
        total_sum = 0.0
        for rec in self:
            if rec.dynamic_filtered_payslip_lines:
                for data in rec.dynamic_filtered_payslip_lines:
                    code = data.category_id.code
                    total_sum += data.total if code == "BON" else 0
                rec['total_additions'] = total_sum
            else:
                rec['total_additions'] = 0.0

    @api.depends('payslip_line_id')
    def _compute_total_substractions(self):
        total_sum = 0.0
        for rec in self:
            if rec.dynamic_filtered_payslip_lines:
                for data in rec.dynamic_filtered_payslip_lines:
                    code = data.category_id.code
                    total_sum += data.total if code == "DED" or code == "PREST" else 0
                rec['total_substractions'] = total_sum
            else:
                rec['total_substractions'] = 0.0

    @api.onchange('total_additions', 'total_substractions')
    def _compute_total_sum(self):
        for rec in self:
            rec.total_sum = rec.total_additions - rec.total_substractions
