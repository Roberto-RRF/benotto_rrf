"""
Author: Roberto Requejo Fernández
Date: [11-12-2024]
GitHub: https://github.com/Roberto-RRF
"""

from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderBomWizard(models.TransientModel):
    _name = 'purchase.order.bom.wizard'
    _description = 'Wizard to Add BOM to Purchase Order'

    mrp_bom_id = fields.Many2one('mrp.bom', string="Producto a Fabricar")

    quantity = fields.Integer(string="Cantidad", default=1)

    line_wizard_ids = fields.One2many('purchase.order.bom.line.wizard', 'wizard_id', string="Lines")

    order_id = fields.Many2one('purchase.order', string="Purchase Order")
    supplier_id = fields.Many2one('res.partner', string="Supplier")

    def default_get(self, fields):
        res = super(PurchaseOrderBomWizard, self).default_get(fields)
        order_id = self.env['purchase.order'].browse(self.env.context.get('order_id'))
        res['order_id'] = order_id.id
        res['supplier_id'] = order_id.partner_id.id
        return res
    
    @api.onchange('quantity')
    def _onchange_quantity(self):
        
        if self.quantity and self.line_wizard_ids:
            for line in self.line_wizard_ids:
                line.quantity_required = line.base_quantity_required * self.quantity

    @api.onchange('mrp_bom_id')
    def on_change_bom(self):
        self.line_wizard_ids = [(5, 0, 0)]
        if self.mrp_bom_id:
            mrp_bom = self.mrp_bom_id
            if mrp_bom:
                lines = []
                for bom_line in mrp_bom.bom_line_ids:                    
                    suppliers = bom_line.product_id.seller_ids.mapped('partner_id')
                    suppliers = suppliers.filtered(lambda s: s.id == self.supplier_id.id)
                    default_supplier = suppliers[:1].id if suppliers else False

                    if suppliers:

                        lines.append((0, 0, {
                            'product_id': bom_line.product_id,
                            'quantity_required': bom_line.product_qty,
                            'supplier_id': default_supplier,
                            'suppliers':suppliers,
                            'base_quantity_required':bom_line.product_qty,
                        }))
                if lines:
                    self.line_wizard_ids = lines
                else:
                    raise UserError("No hay proveedores que coincidan con el proveedor de la orden de compra.")

    def action_add_po_lines(self):
        if not self.line_wizard_ids:
            raise UserError("No hay líneas para agregar a la orden de compra.")
        for line in self.line_wizard_ids:
            if line.product_id and line.supplier_id:
                description = "{} \nLdM: {}. Cant.{}".format(
                    line.product_id.name,
                    self.mrp_bom_id.product_tmpl_id.name,
                    self.quantity,
                )
                self.env['purchase.order.line'].create({
                    'order_id': self.order_id.id,
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity_required,
                    'price_unit': line.product_id.standard_price,
                    'product_uom': line.product_id.uom_po_id.id,
                    'name': description,
                    'partner_id': line.supplier_id.id,
                })
        return {'type': 'ir.actions.act_window_close'}
