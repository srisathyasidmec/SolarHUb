from odoo import models, fields, api


class Inverter(models.Model):
    _name = 'inverter'
    _description = 'Inverter'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    inverter_sequence= fields.Char("Inverter Sequence", default="NEW")

    company_name = fields.Char("Company Name")
    inverter_type=fields.Char("Inverter Type")
    price = fields.Float("Price")
    available_stocks = fields.Integer("Available Stocks")

    model = fields.Char("Model Name")
    capacity = fields.Float("Capacity (Kwh)")
    # taxes = fields.Many2many("account.tax","Tax")
    warrantycover=fields.Boolean("Warranty Covered")

    serial = fields.Char("Serial Number")
    efficiency = fields.Float("Efficiency (Kwh)")
    warrantynotcover=fields.Boolean("Warranty not covered")

    @api.model
    def create(self, vals):
        vals["inverter_sequence"] = self.env['ir.sequence'].next_by_code('inverter')
        product = {'name': vals['inverter_sequence'],
                   'type': 'consu',
                   'solarhub_type': 'inverter',
                   'list_price': vals['price']}

        self.env['product.product'].create(product)
        return super(Inverter, self).create(vals)

    @api.model
    def write(self, vals):
        inverter_sequence = vals.get('inverter_sequence', self.inverter_sequence)
        price = vals.get('price')

        if inverter_sequence and price is not None:
            # Search the product.template with matching name or reference (adapt field as needed)
            template = self.env['product.template'].search([('name', '=', inverter_sequence)], limit=1)
            if template:
                template.list_price = price

        return super(Inverter, self).write(vals)