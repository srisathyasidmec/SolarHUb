from odoo import models, fields, api
from datetime import date

class SolarBattery(models.Model):
    _name = 'contact.diary'
    _description = 'contact diary'
    _rec_name = "contact_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    contact_name=fields.Char("NAME")
    contact_email=fields.Char("EMAIL")
    contact_number=fields.Char("CONTACT NUMBER")
    subject=fields.Char("SUBJECT")
    message=fields.Text("MESSAGE")

    created_date = fields.Date("Created Date", default=fields.Date.today)