from odoo import models, fields, api


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
    tax=fields.Many2many("account.tax","Tax")
    total_cost = fields.Integer("Total Cost")
    availablestock = fields.Integer("Available Stock")
    warrantycover = fields.Boolean("Warranty Covered")
    warrantynotcover = fields.Boolean("Warranty not covered")


    def create(self, vals):
        vals["battery_sequence"] = self.env['ir.sequence'].next_by_code('solar.battery')
        return super(SolarBattery, self).create(vals)
