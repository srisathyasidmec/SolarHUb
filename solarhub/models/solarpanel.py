from odoo import models, fields, api


class SolarPanel(models.Model):
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
    # taxes=fields.Many2many("account.tax","Tax")
    # tax=fields.Many2many("account.tax", string:"Tax")
    tax_ids=fields.Many2many("account.tax",string="Tax")
    total_cost=fields.Integer("Total Cost")
    availablestock=fields.Integer("Available Stock")
    energyproduce=fields.Integer("Energy Produced")
    energyconsume=fields.Integer("Energy Consumed")
    batterystorage=fields.Integer("Battery Storage")
    gridexport=fields.Integer("Grid Export")
    warrantycover=fields.Boolean("Warranty Covered")
    warrantynotcover=fields.Boolean("Warranty not covered")

    @api.model
    def create(self, vals):
        vals["solar_sequence"] = self.env['ir.sequence'].next_by_code('solar.panel')
        product = {'name':vals['solar_sequence'],
                    'type': 'consu',
                   'solarhub_type': 'solar panel',
                   'list_price':vals['price']}
        self.env['product.product'].create(product)

        return super(SolarPanel, self).create(vals)

    @api.model
    def write(self, vals):
        solar_sequence = vals.get('solar_sequence', self.solar_sequence)
        price = vals.get('price')

        if solar_sequence and price is not None:
            # Search the product.template with matching name or reference (adapt field as needed)
            template = self.env['product.template'].search([('name', '=', solar_sequence)], limit=1)
            if template:
                template.list_price = price

        return super(SolarPanel, self).write(vals)



