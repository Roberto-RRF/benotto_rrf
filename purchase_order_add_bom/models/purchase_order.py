from odoo import _, models, fields
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

# class PurchaseOrderLine(models.Model):
#     _inherit = 'import.product'

    

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def action_add_from_bom(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lista de componentes',
            'res_model': 'purchase.order.bom.wizard',
            'view_mode': 'form',
            'target': 'new',
            # 'context': {
            #     'default_order_id': order.id,
            #     'default_supplier_id': supplier_id.id,
            # }
        }
