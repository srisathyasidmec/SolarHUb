from odoo import models, fields, api


class SolarPanel(models.Model):
    _name = 'solar.panel'
    _description = 'Solar Panel'
    _rec_name="company_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_sequence= fields.Char("SOLAR PANEL", default="NEW")

    company_name = fields.Char("Company Name",required=True)
    model = fields.Char("Model Name",required=True)
    serial = fields.Many2many("stock.lot", string="Serial Number")
    panel = fields.Char("Panel Type")
    wattage= fields.Integer( "Wattage")
    voltage = fields.Float("Voltage")
    current=fields.Float("Current")
    degrade=fields.Float("Degradation rate")
    price=fields.Float("Price")
    tax_ids=fields.Many2many("account.tax",string="Tax")
    total_cost=fields.Float("Total Cost",compute="compute_total_cost")
    availablestock=fields.Integer("Available Stock")
    energyproduce=fields.Integer("Energy Produced")
    energyconsume=fields.Integer("Energy Consumed")
    batterystorage=fields.Integer("Battery Storage")
    gridexport=fields.Integer("Grid Export")
    warrantycover=fields.Boolean("Warranty Covered")
    years_of_Warranty = fields.Integer("Years Of Warranty")
    status = fields.Selection([("available", "Available"), ("unavailable", "Unavailable")], "Status",compute="compute_status")

    @api.model
    def create(self, vals):
        vals["solar_sequence"] = self.env['ir.sequence'].next_by_code('solar.panel')
        product = {'name':vals['solar_sequence'],
                    'type': 'consu',
                   'solarhub_type': 'solar panel',
                   'list_price':vals['price'],
                   'taxes_id':vals['tax_ids'],
                   # 'is_storable':'lot',
                   }
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

    @api.depends('price', 'tax_ids')
    def compute_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            rec.total_cost = rec.price + (rec.price * total_tax_percent / 100)

    @api.depends('availablestock')
    def compute_status(self):
        for i in self:
            if i.availablestock > 0:
                i.status="available"
            else:
                i.status="unavailable"