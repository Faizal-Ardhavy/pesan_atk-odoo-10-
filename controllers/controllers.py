# -*- coding: utf-8 -*-
from odoo import http

# class PesanAtk(http.Controller):
#     @http.route('/pesan_atk/pesan_atk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pesan_atk/pesan_atk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pesan_atk.listing', {
#             'root': '/pesan_atk/pesan_atk',
#             'objects': http.request.env['pesan_atk.pesan_atk'].search([]),
#         })

#     @http.route('/pesan_atk/pesan_atk/objects/<model("pesan_atk.pesan_atk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pesan_atk.object', {
#             'object': obj
#         })