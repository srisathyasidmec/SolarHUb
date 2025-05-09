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
    # tax = fields.Many2many("account.tax","Tax")
    tax_ids = fields.Many2many("account.tax", string="Tax")
    warrantycover=fields.Boolean("Warranty Covered")

    serial = fields.Char("Serial Number")
    efficiency = fields.Float("Efficiency (Kwh)")
    warrantynotcover=fields.Boolean("Warranty not covered")

    @api.model
    def create(self, vals):
        vals["inverter_sequence"] = self.env['ir.sequence'].next_by_code('inverter')
        return super(Inverter, self).create(vals)