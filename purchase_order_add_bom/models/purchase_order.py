from odoo import _, models, fields
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def action_add_from_bom(self):
        order_id = self.order_id.id
        purchase_order = self.env['purchase.order'].search([('id', '=', order_id)], limit=1)
        supplier_id = purchase_order.partner_id.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lista de componentes',
            'res_model': 'purchase.order.bom.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': order_id,
                'default_supplier_id': supplier_id,
            }
        }
