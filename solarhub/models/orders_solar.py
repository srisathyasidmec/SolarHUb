from odoo import fields, models, api
from datetime import date

class OrdersSolar(models.Model):
    _name = "orders.solar"
    _rec_name = "solar_order_sequence"
    _description = "SolarHub Orders"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    solar_order_sequence= fields.Char("SOLAR PANEL", default="NEW")

    status = fields.Selection([("pending", "Pending"), ("completed", "Completed")], "status",compute='status_date')

    customer_name = fields.Many2one('res.partner', 'Customer', required=True)
    load_demand = fields.Float('Load Demand(kg)')
    installation_date = fields.Date('Installation Date')

    service_type = fields.Many2one("system.service", "Service Type")
    order_date = fields.Date("Order Date", default=date.today() ,required=True)
    employee_ids = fields.Many2many("hr.employee", string="Employee", required=True)

    property_type = fields.Many2one("system.property", "Property Type")
    delivery_date = fields.Date("Delivery Date")
    assign_user = fields.Many2one("res.users", "Assign User", required=True)

    description = fields.Text(string="Description")

    solar_lines = fields.One2many("solar.orders.lines", "solar_order", "Solar Order Lines")
    battery_lines = fields.One2many("battery.orders.lines",inverse_name="battery_order",string="Battery Order Lines")
    inverter_lines = fields.One2many("inverter.orders.lines",inverse_name="inverter_order",string="Inverter Order Lines")

    solar_sub_total = fields.Float(string='Total Assurance', compute='compute_solar_total')
    battery_sub_total = fields.Float(string='Total Battery', compute='compute_battery_total')
    inverter_sub_total = fields.Float(string='Total Inverter', compute='compute_inverter_total')

    grandtotal = fields.Float(string="grand Total", compute="compute_grand_total")

    @api.depends('solar_lines.solar_price')
    def compute_solar_total(self):
        for order in self:
            order.solar_sub_total = sum(line.solar_sub_total for line in order.solar_lines)
    @api.depends('battery_lines.battery_price')
    def compute_battery_total(self):
        for order in self:
            order.battery_sub_total = sum(line.battery_sub_total for line in order.battery_lines)
    @api.depends('battery_lines.battery_price')
    def compute_inverter_total(self):
        for order in self:
            order.inverter_sub_total = sum(line.inverter_sub_total for line in order.inverter_lines)

    @api.depends('solar_sub_total','battery_sub_total','inverter_sub_total')
    def compute_grand_total(self):
        for order in self:
            order.grandtotal = order.solar_sub_total + order.battery_sub_total + order.inverter_sub_total

    def status_date(self):
        today = date.today()
        for i in self:
            if i.installation_date and today > i.installation_date:
                i.status = 'completed'
            else:
                i.status = 'pending'

    @api.model
    def create(self, vals):
        vals["solar_order_sequence"] = self.env['ir.sequence'].next_by_code('orders.solar')
        return super(OrdersSolar, self).create(vals)

#
class SolarOrdersLines(models.Model):
    _name = "solar.orders.lines"

    solar_panel = fields.Many2one("solar.panel", "Solar Panel")
    tax_ids = fields.Many2many("account.tax", string="Tax")
    solar_price = fields.Float("Price")
    solar_total_cost = fields.Float("Total Cost", compute="compute_solar_total_cost")
    solar_quantity = fields.Integer("Quantity", default="1")
    solar_order = fields.Many2one("orders.solar", "Solar Orders")
    solar_sub_total = fields.Float("Sub Total",compute="compute_solar_subtotal")

    @api.onchange("solar_panel")
    def solar_details(self):
        for rec in self:
            rec.solar_price = rec.solar_panel.price
            rec.tax_ids = rec.solar_panel.tax_ids
            rec.solar_total_cost = rec.solar_panel.total_cost

    @api.depends('solar_price', 'tax_ids','solar_quantity')
    def compute_solar_total_cost(self):
        for rec in self:
            sub = rec.solar_price * rec.solar_quantity
            total_tax_percent = sum(rec.tax_ids.mapped('amount'))
            tax_amount = sub * (total_tax_percent / 100)
            rec.solar_total_cost = sub + tax_amount

    @api.depends("solar_total_cost")
    def compute_solar_subtotal(self):
        for rec in self:
            rec.solar_sub_total += rec.solar_total_cost


class BatteryOrdersLines(models.Model):
    _name = "battery.orders.lines"

    battery_id = fields.Many2one("solar.battery","Battery")
    battery_tax_ids = fields.Many2many("account.tax", string="Tax")
    battery_price = fields.Float("Price")
    battery_total_cost = fields.Float("Total Cost", compute="compute_battery_total_cost")
    battery_quantity = fields.Integer("Quantity", default="1")
    battery_order = fields.Many2one("orders.solar", "Battery Orders")
    battery_sub_total = fields.Float("Sub Total", compute="compute_battery_subtotal")

    @api.onchange("battery_id")
    def solar_details(self):
        for rec in self:
            rec.battery_price = rec.battery_id.price
            rec.battery_tax_ids = rec.battery_id.tax_ids
            rec.battery_total_cost = rec.battery_id.total_cost

    @api.depends('battery_price', 'battery_tax_ids', 'battery_quantity')
    def compute_battery_total_cost(self):
        for rec in self:
            sub = rec.battery_price * rec.battery_quantity
            total_tax_percent = sum(rec.battery_tax_ids.mapped('amount'))
            tax_amount = sub * (total_tax_percent / 100)
            rec.battery_total_cost = sub + tax_amount

    @api.depends("battery_total_cost")
    def compute_battery_subtotal(self):
        for rec in self:
            rec.battery_sub_total += rec.battery_total_cost


class InverterOrdersLines(models.Model):
    _name = "inverter.orders.lines"

    inverter_id = fields.Many2one(comodel_name="inverter", string="Inverter")
    inverter_tax_ids = fields.Many2many("account.tax", string="Tax")
    inverter_price = fields.Float("Price")
    inverter_total_cost = fields.Float("Total Cost", compute="compute_inverter_total_cost")
    inverter_quantity = fields.Integer("Quantity", default="1")
    inverter_order = fields.Many2one("orders.solar", "Battery Orders")
    inverter_sub_total = fields.Float("Sub Total", compute="compute_inverter_subtotal")

    @api.onchange("inverter_id")
    def battery_details(self):
        for rec in self:
            rec.inverter_price = rec.inverter_id.price
            rec.inverter_tax_ids = rec.inverter_id.tax_ids
            rec.inverter_total_cost = rec.inverter_id.total_cost

    @api.depends('inverter_price', 'inverter_tax_ids', 'inverter_quantity')
    def compute_inverter_total_cost(self):
        for rec in self:
            sub = rec.inverter_price * rec.inverter_quantity
            total_tax_percent = sum(rec.inverter_tax_ids.mapped('amount'))
            tax_amount = sub * (total_tax_percent / 100)
            rec.inverter_total_cost = sub + tax_amount

    @api.depends("inverter_total_cost")
    def compute_inverter_subtotal(self):
        for rec in self:
            rec.inverter_sub_total += rec.inverter_total_cost