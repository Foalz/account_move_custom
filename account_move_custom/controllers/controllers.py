# -*- coding: utf-8 -*-
# from odoo import http


# class AccountMoveCustom(http.Controller):
#     @http.route('/account_move_custom/account_move_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_move_custom/account_move_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_move_custom.listing', {
#             'root': '/account_move_custom/account_move_custom',
#             'objects': http.request.env['account_move_custom.account_move_custom'].search([]),
#         })

#     @http.route('/account_move_custom/account_move_custom/objects/<model("account_move_custom.account_move_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_move_custom.object', {
#             'object': obj
#         })
