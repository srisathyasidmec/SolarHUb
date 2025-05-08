from odoo import models, fields, api


class TaskCustomer(models.Model):
    _name = 'solar.panel'
    _description = 'solar panel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_sequence= fields.Char("patient sequence")

    company_name = fields.Char("Company name")
    model = fields.Text("Model name")
    serial = fields.Text("Serial number")
    panel = fields.Char("panel type")
    wattage= fields.Integer( "Wattage")
    voltage = fields.Integer("Company")
    current=fields.Integer("Current")
    degrade=fields.Integer("Degradation rate")
    price=fields.Integer("Price")
    # tax=fields.Many2one("Tax")
    total_cost=fields.Integer("Total_cost")
    availablestock=fields.Integer("Available_stock")
    energyproduce=fields.Integer("Energy_produced")
    energyconsume=fields.Integer("Energy_consumed")
    batterystorage=fields.Integer("Battery_storage")
    gridexport=fields.Integer("Grid_export")
    warrantycover=fields.Text("warranty_covered")
    warrantynotcover=fields.Text("Warranty not covered")

