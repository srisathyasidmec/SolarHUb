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

    sub_total = fields.Float(string='Total Assurance', compute='compute_solar_total')

    @api.depends('solar_lines.solar_price')
    def compute_solar_total(self):
        for order in self:
            order.sub_total = sum(line.sub_total for line in order.solar_lines)


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

    sub_total = fields.Float("Sub Total",compute="compute_solar_subtotal")

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
            rec.sub_total += rec.solar_total_cost