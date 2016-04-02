# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class saudi_egy_shipment(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'picking_type_id': fields.many2one('stock.picking.type', 'Picking Type', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, required=True),
        'picking_type_code': fields.related('picking_type_id', 'code', type='char', string='Picking Type Code', help="Technical field used to display the correct label on print button in the picking view"),
        'driver_id': fields.char('Driver Name', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},),
        'license_no': fields.char('License Number', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'mobile_no_sudan': fields.integer('Mobile Number Sudan', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'mobile_no_egy': fields.integer('Mobile Number Egypt', states={'done': [('readonly', True)],'cancel': [('readonly', True)]}),
        'truck_no': fields.char('Truck Number', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'departure_date': fields.datetime('Departure Date', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'expected_date': fields.datetime('Expected Date',  states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'watsh_id': fields.char('Cattle Man',  states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
        'tracking_no': fields.char('Tracking Number', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}),
    }


class stock_shipment(osv.osv):
    _name = 'stock.picking.type'
    _inherit = 'stock.picking.type'
    _columns = {
        'code': fields.selection([('incoming', 'Suppliers'), ('outgoing', 'Customers'), ('internal', 'Internal'),('egy', 'Egypt Shipment'),('saudi', 'Saudi Arabia Shipment')], 'Type of Operation', required=True),
    }