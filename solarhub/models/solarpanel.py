from odoo import models, fields, api


class SolarCustomer(models.Model):
    _name = 'solar.panel'
    _description = 'solar panel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_sequence= fields.Char("solar sequence")

    company_name = fields.Char("Company name")
    model = fields.Char("Model name")
    serial = fields.Char("Serial number")
    panel = fields.Char("panel type")
    wattage= fields.Integer( "Wattage")
    voltage = fields.Integer("Voltage")
    current=fields.Integer("Current")
    degrade=fields.Integer("Degradation rate")
    price=fields.Integer("Price")
    # tax=fields.Many2one("Tax")
    total_cost=fields.Integer("Total cost")
    availablestock=fields.Integer("Available stock")
    energyproduce=fields.Integer("Energy produced")
    energyconsume=fields.Integer("Energy consumed")
    batterystorage=fields.Integer("Battery storage")
    gridexport=fields.Integer("Grid export")
    warrantycover=fields.Boolean("Warranty covered")
    warrantynotcover=fields.Boolean("Warranty not covered")

