from odoo import fields, models, api

class SolarHubOrders(models.Model):
    _name = 'solarhub.order'
    _description = 'Solar Hub Order'
    _rec_name = 'solar_order_sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_order_sequence= fields.Char("SOLAR PANEL", default="NEW")

    customer_name = fields.Many2one('res.partner', 'Customer')
    load_demand = fields.Float('Load Demand(kg)')
    installation_date =fields.Date('Installation Date')

    service_type = fields.Many2one("system.service", "Service Type")
    order_date = fields.Date("Order Date")
    employee_ids = fields.Many2many("hr.employee", string="Employee")

    property_type = fields.Many2one("system.property","Property Type")
    delivery_date = fields.Date("Delivery Date")
    assign_user = fields.Many2one("res.users", "Assign User")

    description = fields.Text(string="Description")

    solar_panel = fields.Many2one("solar.panel", "Solar Panel")
    tax_ids = fields.Many2many("account.tax", string="Tax")

    solar_price = fields.Float("Price")
    solar_total_cost = fields.Float("Total Cost")

    solar_quantity = fields.Integer("Quantity", default="1")

    battery_id = fields.Many2one("solar.battery")
    # battery_tax_ids = fields.Many2many("account.tax", string="Tax")

    battery_price = fields.Float("Price")
    battery_total_cost = fields.Float("Total Cost")

    battery_quantity = fields.Integer("Quantity", default="1")

    inverter_id = fields.Many2one(comodel_name="inverter",string="Inverter")
    # inverter_tax_ids = fields.Many2many("account.tax",string="Tax")

    inverter_price = fields.Float("Price")
    inverter_total_cost = fields.Float("Total Cost")

    inverter_quantity = fields.Integer("Quantity")


    solarorder_lines = fields.One2many("solarhub.order.lines", "solar_order", "Extra Order lines")


    @api.model
    def create(self, vals):
        vals["solar_order_sequence"] = self.env['ir.sequence'].next_by_code('solarhub.order')
        return super(SolarHubOrders, self).create(vals)

class SolarHubOrderLines(models.Model):
    _name = "solarhub.order.lines"

    # Inverter Detail
    assurance_type = fields.Many2one("system.assurance", "ASSURANCE TYPE")
    sub_type = fields.Many2one("assurance.subtype", "SUB TYPE")
    inverter_detail_quantity = fields.Integer("QUANTITY")
    inverter_detail_price = fields.Float("PRICE")
    solar_order = fields.Many2one("solarhub.order", "Extra Orders")