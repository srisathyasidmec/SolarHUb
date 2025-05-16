from odoo import models, fields, api


class Inverter(models.Model):
    _name = 'inverter'
    _description = 'Inverter'
    # _rec_name="inverter_type"
    _rec_name = 'company_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    inverter_sequence= fields.Char("Inverter Sequence", default="NEW")

    company_name = fields.Char("Company Name",required=True)
    inverter_type=fields.Char("Inverter Type",required=True)
    price = fields.Float("Price")
    available_stocks = fields.Integer("Available Stocks")

    model = fields.Char("Model Name")
    capacity = fields.Float("Capacity (Kwh)")
    # taxes = fields.Many2many("account.tax","Tax")
    # tax = fields.Many2many("account.tax","Tax")
    tax_ids = fields.Many2many("account.tax", string="Tax")
    warrantycover=fields.Boolean("Warranty Covered")
    years_of_Warranty = fields.Integer("Years Of Warranty")

    serial = fields.Many2many("stock.lot",string="Serial Number")
    efficiency = fields.Float("Efficiency (Kwh)")
    total_cost = fields.Float("Total Cost",compute="compute_total_cost")
    status = fields.Selection([("available", "Available"), ("unavailable", "Unavailable")], "Status",compute="compute_status")


    @api.model_create_multi
    def create(self, vals):
        vals["inverter_sequence"] = self.env['ir.sequence'].next_by_code('inverter')
        product = {'name': vals['inverter_sequence'],
                   'type': 'consu',
                   'solarhub_type': 'inverter',
                   'list_price': vals['price'],
                   'taxes_id':vals['tax_ids']}

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

    @api.depends('price', 'tax_ids')
    def compute_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            rec.total_cost = rec.price + (rec.price * total_tax_percent / 100)

    @api.depends('available_stocks')
    def compute_status(self):
        for i in self:
            if i.available_stocks > 0:
                i.status = "available"
            else:
                i.status = "unavailable"
