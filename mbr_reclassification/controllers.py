# -*- coding: utf-8 -*-
from openerp import http

# class MbrMbr(http.Controller):
#     @http.route('/mbr_mbr/mbr_mbr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mbr_mbr/mbr_mbr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mbr_mbr.listing', {
#             'root': '/mbr_mbr/mbr_mbr',
#             'objects': http.request.env['mbr_mbr.mbr_mbr'].search([]),
#         })

#     @http.route('/mbr_mbr/mbr_mbr/objects/<model("mbr_mbr.mbr_mbr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mbr_mbr.object', {
#             'object': obj
#         })