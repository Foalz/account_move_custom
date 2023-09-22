# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/payrollCustom(http.Controller):
#     @http.route('//mnt/extra-addons/payroll_custom//mnt/extra-addons/payroll_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/payroll_custom//mnt/extra-addons/payroll_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/payroll_custom.listing', {
#             'root': '//mnt/extra-addons/payroll_custom//mnt/extra-addons/payroll_custom',
#             'objects': http.request.env['/mnt/extra-addons/payroll_custom./mnt/extra-addons/payroll_custom'].search([]),
#         })

#     @http.route('//mnt/extra-addons/payroll_custom//mnt/extra-addons/payroll_custom/objects/<model("/mnt/extra-addons/payroll_custom./mnt/extra-addons/payroll_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/payroll_custom.object', {
#             'object': obj
#         })
