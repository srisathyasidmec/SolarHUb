from odoo import models, fields, api
from odoo.osv import expression

class Maintenance(models.Model):
    _name = "solar.maintenance"
    _description = 'Maintenance'
    _rec_name = "subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer = fields.Many2one("res.partner",string="Customer")
    subject = fields.Char(string="Subject")
    delivery_date = fields.Date("Delivery Date")
    description =  fields.Text("Description")

    order = fields.Many2one("solarhub.order",string="Order")
    requests_date = fields.Date("Requests Date")
    maintenance_fee = fields.Selection(selection=[('paid','Paid'),('free','Free')], string="Maintenance")