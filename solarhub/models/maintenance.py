from odoo import models, fields, api
from datetime import date
from odoo.osv import expression



class Maintenance(models.Model):
    _name = "solar.maintenance"
    _description = 'Maintenance'
    _rec_name = "subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_email = fields.Char("Customer Email")
    customer = fields.Many2one("res.partner",string="Customer",required="true")
    subject = fields.Char(string="Subject")
    delivery_date = fields.Date("Delivery Date")
    description =  fields.Text("Description")

    company_id = fields.Many2one("res.company", "Company Name")
    user = fields.Many2one("res.users", "User")


    order = fields.Many2one("solarhub.order",string="Order")
    requests_date = fields.Date("Requests Date")
    maintenance_fee = fields.Selection(selection=[('paid','Paid'),('free','Free')], string="Maintenance")
    status = fields.Selection([("pending", "Pending"), ("completed", "Completed")], "status",compute='status_date')

    def status_date(self):
        today = date.today()
        for i in self:
            if i.delivery_date and today > i.delivery_date:
                i.status = 'completed'
            else:
                i.status = 'pending'

    def send_email(self):
        for rec in self:
            template = self.env.ref("solarhub.mail_template_maintenance_confirm")
            template.send_mail(rec.id, force_send=True)