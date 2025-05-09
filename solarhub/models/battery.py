import typing

from odoo import models, fields, api
from odoo.api import ValuesType


class SolarBattery(models.Model):
    _name = 'solar.battery'
    _description = 'solar battery'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    battery_sequence=fields.Char("BATTERY", default="NEW")

    company_name = fields.Char("Company Name")
    model = fields.Char("Model Name")
    serial = fields.Char("Serial Number")
    price = fields.Integer("Price")
    battery_type=fields.Char("Battery Type")
    capacity=fields.Char("Capacity")
    # taxes=fields.Many2many("account.tax","Tax")
    total_cost = fields.Integer("Total Cost")
    availablestock = fields.Integer("Available Stock")
    warrantycover = fields.Boolean("Warranty Covered")
    warrantynotcover = fields.Boolean("Warranty not covered")


    @api.model
    def create(self, vals):
        vals["battery_sequence"] = self.env['ir.sequence'].next_by_code('solar.battery')
        product = {'name': vals['battery_sequence'],
                   'type': 'consu',
                   'solarhub_type':'battery',
                   'list_price': vals['price']}

        self.env['product.product'].create(product)
        return super(SolarBattery, self).create(vals)

    # @api.model
    # def write(self, vals):
    #     product = {'name': vals['battery_sequence'],
    #                'list_price': vals['price']}
    #     self.env['product.product'].write(product)
    #     return super(SolarBattery, self).write(vals)

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