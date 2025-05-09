from odoo import models, fields, api


class SolarBattery(models.Model):
    _name = 'solar.battery'
    _description = 'solar battery'
    # _rec_name="battery_type"
    _rec_name = 'battery_sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    battery_sequence=fields.Char("BATTERY", default="NEW")
    company_name = fields.Char("Company Name")
    model = fields.Char("Model Name")
    serial = fields.Char("Serial Number")
    price = fields.Float("Price")
    battery_type=fields.Char("Battery Type")
    capacity=fields.Char("Capacity")
    tax_ids = fields.Many2many("account.tax", string="Tax")
    total_cost = fields.Float("Total Cost",compute='compute_total_cost')
    availablestock = fields.Integer("Available Stock")
    warrantycover = fields.Boolean("Warranty Covered")
    warrantynotcover = fields.Boolean("Warranty not covered")

    @api.model
    def create(self, vals):
        vals["battery_sequence"] = self.env['ir.sequence'].next_by_code('solar.battery')
        product = {'name': vals['battery_sequence'],
                   'type': 'consu',
                   'solarhub_type':'battery',
                   'list_price': vals['price'],
                   'taxes_id':vals['tax_ids']}

        self.env['product.product'].create(product)
        return super(SolarBattery, self).create(vals)

    @api.model
    def write(self, vals):
        battery_sequence = vals.get('battery_sequence', self.battery_sequence)
        price = vals.get('price')

        if battery_sequence and price is not None:
            # Search the product.template with matching name or reference (adapt field as needed)
            template = self.env['product.template'].search([('name', '=', battery_sequence)], limit=1)
            if template:
                template.list_price = price

        return super(SolarBattery, self).write(vals)

    @api.depends('price', 'tax_ids')
    def compute_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            rec.total_cost = rec.price + (rec.price * total_tax_percent / 100)