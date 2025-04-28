from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderBomLineWizard(models.TransientModel):
    _name = 'purchase.order.bom.line.wizard'
    _description = 'Wizard to Manage BOM Lines for Purchase Orders'

    product_id = fields.Many2one('product.product', string='Product')
    supplier_id = fields.Many2one('res.partner', string='Supplier', )
    suppliers = fields.Many2many('res.partner', string='Supplier')
    base_quantity_required = fields.Float(string='Base Quantity Required')
    quantity_required = fields.Float(string='Quantity Required')
    wizard_id = fields.Many2one('purchase.order.bom.wizard')