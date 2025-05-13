from odoo import fields, models, api
from datetime import date

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
    solar_total_cost = fields.Float("Total Cost",compute="compute_solar_total_cost")

    solar_quantity = fields.Integer("Quantity", default="1")

    battery_id = fields.Many2one("solar.battery")
    battery_tax_ids = fields.Many2many("account.tax", string="Tax", relation="solarhub_order_battery_tax_rel")

    battery_price = fields.Float("Price")
    battery_total_cost = fields.Float("Total Cost",compute="compute_battery_total_cost")

    battery_quantity = fields.Integer("Quantity", default="1")

    inverter_id = fields.Many2one(comodel_name="inverter",string="Inverter")
    inverter_tax_ids = fields.Many2many("account.tax",string="Tax", relation="solarhub_order_inverter_tax_rel")

    inverter_price = fields.Float("Price")
    inverter_total_cost = fields.Float("Total Cost",compute="compute_inverter_total_cost")

    inverter_quantity = fields.Integer("Quantity")

    solarorder_lines = fields.One2many("solarhub.order.lines", "solar_order", "Extra Order lines")
    status = fields.Selection([("pending", "Pending"), ("completed", "Completed")], "status",compute='status_date')


    subtotal=fields.Float("SubTotal",compute="compute_total")
    taxtotal=fields.Float("Tax Total",compute="compute_total")
    grandtotal = fields.Float(string="grand Total", compute="compute_total")

    @api.model
    def create(self, vals):
        vals["solar_order_sequence"] = self.env['ir.sequence'].next_by_code('solarhub.order')
        return super(SolarHubOrders, self).create(vals)

    @api.depends('battery_price', 'tax_ids')
    def compute_battery_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.battery_tax_ids.mapped('amount'))
            rec.battery_total_cost = rec.battery_price + (rec.battery_price * total_tax_percent / 100)

    @api.depends('solar_price', 'tax_ids')
    def compute_solar_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            rec.solar_total_cost = rec.solar_price + (rec.solar_price * total_tax_percent / 100)

    @api.depends('inverter_price', 'tax_ids')
    def compute_inverter_total_cost(self):
        for rec in self:
            total_tax_percent = sum(rec.inverter_tax_ids.mapped('amount'))
            rec.inverter_total_cost = rec.inverter_price + (rec.inverter_price * total_tax_percent / 100)

    def status_date(self):
        today = date.today()
        for i in self:
            if i.installation_date and today > i.installation_date:
                i.status = 'completed'
            else:
                i.status = 'pending'

    @api.onchange("solar_panel","solar_quantity")
    def solar_details(self):
        for rec in self:
            rec.solar_price = rec.solar_panel.price
            rec.tax_ids = rec.solar_panel.tax_ids
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            rec.solar_total_cost = rec.solar_quantity * (rec.solar_price + (rec.solar_price * total_tax_percent / 100))

    @api.onchange("battery_id", "battery_quantity")
    def battery_details(self):
        for rec in self:
            rec.battery_price = rec.battery_id.price
            rec.battery_tax_ids = rec.battery_id.tax_ids
            total_tax_percent = sum(rec.battery_tax_ids.mapped('amount'))
            rec.battery_total_cost = rec.battery_quantity * (rec.battery_price + (rec.battery_price * total_tax_percent / 100))

    @api.onchange("inverter_id", "inverter_quantity")
    def inverter_details(self):
        for rec in self:
            rec.inverter_price = rec.inverter_id.price
            rec.inverter_tax_ids = rec.inverter_id.tax_ids
            total_tax_percent = sum(rec.inverter_tax_ids.mapped('amount'))
            rec.inverter_total_cost = rec.inverter_quantity * (rec.inverter_price + (rec.inverter_price * total_tax_percent / 100))

    @api.onchange('inverter_price', 'battery_price', 'solar_price')
    def compute_total(self):
        for rec in self:
            rec.subtotal = (rec.inverter_price * rec.inverter_quantity) + (rec.battery_price * rec.battery_quantity) + (
                        rec.solar_price * rec.solar_quantity)
            rec.taxtotal = (rec.inverter_total_cost + rec.battery_total_cost + rec.solar_total_cost) - (rec.subtotal)
            rec.grandtotal = rec.subtotal + rec.taxtotal

class SolarHubOrderLines(models.Model):
    _name = "solarhub.order.lines"

    # Inverter Detail
    assurance_type = fields.Many2one("system.assurance", "ASSURANCE TYPE")
    sub_type = fields.Many2one("assurance.subtype", "SUB TYPE")
    inverter_detail_quantity = fields.Integer("QUANTITY")
    inverter_detail_price = fields.Float("PRICE")
    solar_order = fields.Many2one("solarhub.order", "Extra Orders")

    @api.onchange("sub_type","inverter_detail_quantity")
    def change_sub_price(self):
        for rec in self:
            rec.inverter_detail_price = rec.inverter_detail_quantity * rec.sub_type.rate
