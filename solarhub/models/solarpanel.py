from odoo import models, fields, api


class TaskCustomer(models.Model):
    _name = 'solar.panel'
    _description = 'solar panel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_sequence= fields.Char("SOLAR PANEL", default="NEW")

    company_name = fields.Char("Company Name")
    model = fields.Char("Model Name")
    serial = fields.Char("Serial Number")
    panel = fields.Char("Panel Type")
    wattage= fields.Integer( "Wattage")
    voltage = fields.Integer("Voltage")
    current=fields.Integer("Current")
    degrade=fields.Integer("Degradation rate")
    price=fields.Integer("Price")
    tax=fields.Many2many("account.tax", string:"Tax")
    total_cost=fields.Integer("Total Cost")
    availablestock=fields.Integer("Available Stock")
    energyproduce=fields.Integer("Energy Produced")
    energyconsume=fields.Integer("Energy Consumed")
    batterystorage=fields.Integer("Battery Storage")
    gridexport=fields.Integer("Grid Export")
    warrantycover=fields.Boolean("Warranty Covered")
    warrantynotcover=fields.Boolean("Warranty not covered")


    def create(self, vals):
        vals["solar_sequence"] = self.env['ir.sequence'].next_by_code('solar.panel')
        return super(TaskCustomer, self).create(vals)

