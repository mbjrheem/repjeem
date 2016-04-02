# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.float_utils import float_round
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class mbr_mbr(osv.osv):
    _name = 'mbr_mbr.mbr_mbr'

    def _quantity_normalize(self, cr, uid, ids, name, args, context=None):
        uom_obj = self.pool.get('product.uom')
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            res[m.id] = uom_obj._compute_qty_obj(cr, uid, m.product_uom, m.product_uom_qty, m.product_id.uom_id, context=context)
        return res

    def _set_product_qty(self, cr, uid, id, field, value, arg, context=None):
        """ The meaning of product_qty field changed lately and is now a functional field computing the quantity
            in the default product UoM. This code has been added to raise an error if a write is made given a value
            for `product_qty`, where the same write should set the `product_uom_qty` field instead, in order to
            detect errors.
        """
        raise osv.except_osv(_('Programming Error!'), _('The requested operation cannot be processed because of a programming error setting the `product_qty` field instead of the `product_uom_qty`.'))

    def onchange_uos_quantity(self, cr, uid, ids, product_id, product_uos_qty,
                          product_uos, product_uom):
        """ On change of product quantity finds UoM and UoS quantities
        @param product_id: Product id
        @param product_uos_qty: Changed UoS Quantity of product
        @param product_uom: Unit of measure of product
        @param product_uos: Unit of sale of product
        @return: Dictionary of values
        """
        result = {
            'product_uom_qty': 0.00
        }

        if (not product_id) or (product_uos_qty <= 0.0):
            result['product_uos_qty'] = 0.0
            return {'value': result}

        product_obj = self.pool.get('product.product')
        uos_coeff = product_obj.read(cr, uid, product_id, ['uos_coeff'])

        # No warning if the quantity was decreased to avoid double warnings:
        # The clients should call onchange_quantity too anyway

        if product_uos and product_uom and (product_uom != product_uos):
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
            result['product_uom_qty'] = float_round(product_uos_qty / uos_coeff['uos_coeff'], precision_digits=precision)
        else:
            result['product_uom_qty'] = product_uos_qty
        return {'value': result}

    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,loc_dest_id=False, name = False,new_product_id=False):
        """ On change of product id, if finds UoM, UoS, quantity and UoS quantity.
        @param prod_id: Changed Product id
        @param loc_id: Source location id
        @param loc_dest_id: Destination location id
        @param partner_id: Address id of partner
        @return: Dictionary of values
        """
        if not prod_id:
            return {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        lang = user and user.lang or False
        if prod_id:
            ctx = {'lang': lang}
        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        product2 = self.pool.get('product.product').browse(cr, uid, [new_product_id], context=ctx)[0]
        uos_id = False
        qty = self.pool.get('product.product')._product_available(cr, uid, [prod_id], context=dict({}, location=loc_id))
        newName = " "
        if product2.name:
            newName = "classify" + str(product.name) + " to " + str(product2.name)
        if prod_id in qty:
            qty_wh = qty[prod_id]['qty_available']
        result = {
            'name': newName,
            'qty_available': qty_wh,
            'product_uom': product.uom_id.id,
            'product_uos': uos_id,
            'product_uom_qty': 1.00,
        #    'product_uos_qty': self.pool.get('stock.move').onchange_quantity(self, cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
        }
        if loc_id:
            result['location_id'] = loc_id
        if loc_dest_id:
            result['location_dest_id'] = loc_dest_id
        return {'value': result}

    def onchange_product_id2(self, cr, uid, ids, prod_id=False,name = False,new_product_id=False):

        if not prod_id:
            return {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        lang = user and user.lang or False
        if prod_id:
            ctx = {'lang': lang}
        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        product2 = self.pool.get('product.product').browse(cr, uid, [new_product_id], context=ctx)[0]
        newName = "classify " + str(product.name) + " to " + str(product2.name)
        result = {
            'name': newName,
        }
        return {'value': result}

    def onchange_quantity(self, cr, uid, ids, product_id, product_qty, product_uom, product_uos):
        """ On change of product quantity finds UoM and UoS quantities
        @param product_id: Product id
        @param product_qty: Changed Quantity of product
        @param product_uom: Unit of measure of product
        @param product_uos: Unit of sale of product
        @return: Dictionary of values
        """
        result = {
            'product_uos_qty': 0.00
        }
        warning = {}

        if (not product_id) or (product_qty <= 0.0):
            result['product_qty'] = 0.0
            return {'value': result}

        product_obj = self.pool.get('product.product')
        uos_coeff = product_obj.read(cr, uid, product_id, ['uos_coeff'])

        # Warn if the quantity was decreased
        if ids:
            for move in self.read(cr, uid, ids, ['product_qty']):
                if product_qty < move['product_qty']:
                    warning.update({
                        'title': _('Information'),
                        'message': _("By changing this quantity here, you accept the "
                                "new quantity as complete: Odoo will not "
                                "automatically generate a back order.")})
                break

        if product_uos and product_uom and (product_uom != product_uos):
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product UoS')
            result['product_uos_qty'] = float_round(product_qty * uos_coeff['uos_coeff'], precision_digits=precision)
        else:
            result['product_uos_qty'] = product_qty

        return {'value': result, 'warning': warning}

    def onchange_location_id(self, cr, uid, ids, location_id, product_id):
        if location_id:
            qty_wh = 0.0
            qty = self.pool.get('product.product')._product_available(cr, uid, [product_id], context=dict({}, location=location_id))
            if product_id in qty:
                qty_wh = qty[product_id]['qty_available']
            return { 'value': { 'qty_available': qty_wh } }

    def _get_default_location(self,cr,uid,context=None):
        res = self.pool.get('stock.location').search(cr,uid,[('usage','=','class_location')], context=None)
        return res and res[0] or False

    def _get_discription(self,uid,ids,product_id):

        return False

    _columns = {
        'name': fields.char('Description', readonly=False, recuired=True, states={'done': [('readonly', True)]}),
        'qty_available': fields.float('Quantity Available', readonly=True),
        'create_date': fields.datetime('Creation Date', readonly=True, select=True),
        'date': fields.datetime('Date', required=True, select=True, help="Move date: scheduled date until move is done, then date of actual move processing", states={'done': [('readonly', True)]}),
        'date_expected': fields.datetime('Expected Date', states={'done': [('readonly', True)]}, required=True, select=True, help="Scheduled date for the processing of this move"),
        'product_id': fields.many2one('product.product', 'Product', required=True, select=True, domain=[('type', '<>', 'service')], states={'done': [('readonly', True)]}),
        'new_product_id': fields.many2one('product.product', 'Classify To', required=True, select=True, domain=[('type', '<>', 'service')], states={'done': [('readonly', True)]}),
        'product_uom_qty': fields.float('Quantity to Classify', digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True, states={'done': [('readonly', True)]},
            help="This is the quantity of products from an inventory "
                "point of view. For moves in the state 'done', this is the "
                "quantity of products that were actually moved. For other "
                "moves, this is the quantity of product that is planned to "
                "be moved. Lowering this quantity does not generate a "
                "backorder. Changing this quantity on assigned moves affects "
                "the product reservation, and should be done with care."
        ),
        'product_qty': fields.function(_quantity_normalize, fnct_inv=_set_product_qty, type='float', digits=0, store={
            _name: (lambda self, cr, uid, ids, c={}: ids, ['product_id', 'product_uom', 'product_uom_qty'], 10),
        }, string='Quantity',
            help='Quantity in the default UoM of the product'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure', required=True, states={'done': [('readonly', True)],'draft':[('readonly', False)]}),
        'product_uos_qty': fields.float('Quantity (UOS)', digits_compute=dp.get_precision('Product UoS'), states={'done': [('readonly', True)]}),
        'product_uos': fields.many2one('product.uom', 'Product UOS', states={'done': [('readonly', True)]}),
        'product_tmpl_id': fields.related('product_id', 'product_tmpl_id', type='many2one', relation='product.template', string='Product Template'),
        'location_id': fields.many2one('stock.location', 'Source Location', required=True, select=True, auto_join=True,
                                       states={'done': [('readonly', True)]}, help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations."),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', readonly=True, domain=[('usage','=', 'class_location')], states={'done': [('readonly', True)]}, select=True,
                                            auto_join=True, help="Location where the system will stock the finished products.", ),

        'picking_id': fields.many2one('stock.picking', 'Reference', select=True, states={'done': [('readonly', True)]}),
        'note': fields.text('Notes'),
        'state': fields.selection([('draft', 'New'),
                                   ('cancel', 'Cancelled'),
                                   ('waiting', 'Waiting Another Move'),
                                   ('confirmed', 'Waiting Availability'),
                                   ('assigned', 'Available'),
                                   ('done', 'Done'),
                                   ], 'Status', readonly=True, select=True, copy=False),
        'company_id': fields.many2one('res.company', 'Company', required=False, select=True),

    }

    _defaults = {
        'date': fields.date.context_today,
        'date_expected': fields.date.today(),
        'qty_done': 0,
        'processed': lambda *a: 'false',
        'state': 'draft',
        'invoice_state':'none',
        'location_dest_id': _get_default_location,
        'name':_get_discription,
    }

    """ This function perform stock move to classify products """

    def action_class(self, cr, uid, ids, context=None):
        context = context or {}
        mov_obj = self.pool.get('stock.move')
        q_obj = self.browse(cr, uid, ids, context=context)
    # return a browse record
        for move in self.browse(cr, uid, ids, context=None):
          #  if move.product_uom_qty > move.qty_available:
          #      raise osv.except_osv(_('Warning!'), _('Cannot classified'))
          #  if move.product_uom_qty < move.product_uom_qty:
                move_data = {
                'product_id': move.product_id.id,
                'product_uom_qty': move.product_uom_qty,
                'product_uom': move.product_id.uom_id.id,
                'product_uos_qty': move.product_uos_qty,
                'product_uos':move.product_uos,
                'date': move.date,
                'location_id': move.location_id.id,
                'location_dest_id': move.location_dest_id.id,
                'state': move.state, # set to done if no approval required
                'name': move.name,
                'picking_id': move.picking_id,
                }
            # dict for second movement, from destination to source
                move_data2 = {
                'product_id': move.new_product_id.id,
                'product_uom_qty': move.product_uom_qty,
                'product_uom': move.new_product_id.uom_id.id,
                'product_uos_qty': move.product_uos_qty,
                'product_uos':move.product_uos,
                'date': move.date,
                'location_id': move.location_dest_id.id,
                'location_dest_id': move.location_id.id,
                'state': move.state, # set to done if no approval required
                'name': move.name,
                'picking_id': move.picking_id,
                }
            # check product quantity to classify

            # create records for move and call function action_done() to perform movement
                mov_id = mov_obj.create(cr, uid, move_data, context=context)
                mov2_id = mov_obj.create(cr,uid, move_data2, context=context)
                mov_obj.action_done(cr, uid,mov_id,context=None)
                mov_obj.action_done(cr, uid, mov2_id, context=None)
                move.state = 'done'
                return True

mbr_mbr()

# inherit this model to add new Location usage "class_location" which used for classification operation

class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'
    _columns = {
        'usage': fields.selection([
                        ('supplier', 'Supplier Location'),
                        ('view', 'View'),
                        ('internal', 'Internal Location'),
                        ('customer', 'Customer Location'),
                        ('inventory', 'Inventory'),
                        ('procurement', 'Procurement'),
                        ('production', 'Production'),
                        ('transit', 'Transit Location'),
                        ('class_location', 'classification')],
                'Location Type', required=True,
                help="""* Supplier Location: Virtual location representing the source location for products coming from your suppliers
                       \n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products
                       \n* Internal Location: Physical locations inside your own warehouses,
                       \n* Customer Location: Virtual location representing the destination location for products sent to your customers
                       \n* Inventory: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)
                       \n* Procurement: Virtual location serving as temporary counterpart for procurement operations when the source (supplier or production) is not known yet. This location should be empty when the procurement scheduler has finished running.
                       \n* Production: Virtual counterpart location for production operations: this location consumes the raw material and produces finished products
                    \n* class_location: Virtual location for classification operations

                      """, select=True),
    }
