# -*- coding: utf-8 -*-
from openerp import http

# class SaudiEgyShipment(http.Controller):
#     @http.route('/saudi_egy_shipment/saudi_egy_shipment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/saudi_egy_shipment/saudi_egy_shipment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('saudi_egy_shipment.listing', {
#             'root': '/saudi_egy_shipment/saudi_egy_shipment',
#             'objects': http.request.env['saudi_egy_shipment.saudi_egy_shipment'].search([]),
#         })

#     @http.route('/saudi_egy_shipment/saudi_egy_shipment/objects/<model("saudi_egy_shipment.saudi_egy_shipment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('saudi_egy_shipment.object', {
#             'object': obj
#         })