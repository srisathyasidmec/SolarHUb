from odoo import models,fields,api

class SolarInspection(models.Model):
    _name='solar.inspection'
    _description='solar hub inspection'
    _rec_name='customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_email = fields.Char("Customer Email")
    customer=fields.Many2one("res.partner","Customer",required="true")
    user=fields.Many2one("res.users","User",required="true")
    inspection_date=fields.Date("Inspection Date")
    note=fields.Text("Note")
    order=fields.Many2one("solarhub.order","Order")

    company_id = fields.Many2one("res.company","Company Name")

    @api.onchange("customer")
    def _onchage_customer(self):
        for rec in self:
            rec.customer_email = rec.customer.email

    def send_email(self):
        for rec in self:
            template = self.env.ref("solarhub.mail_template_inspection_confirm")
            template.send_mail(rec.id, force_send=True)