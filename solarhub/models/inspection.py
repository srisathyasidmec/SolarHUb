from odoo import models,fields,api


class SolarInspection(models.Model):
    _name='solar.inspection'
    _description='solar hub inspection'
    _rec_name='customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    customer=fields.Many2one("res.partner","Customer",required="true")
    user=fields.Many2one("res.users","User",required="true")
    inspection_date=fields.Date("Inspection Date")
    note=fields.Text("Note")
    order=fields.Many2one("solarhub.order","Order")

