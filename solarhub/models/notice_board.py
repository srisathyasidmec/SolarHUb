from odoo import models, fields, api
from datetime import date



class SolarBattery(models.Model):
    _name = 'notice.board'
    _description = 'notice board'
    _rec_name="title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")
    date_today = fields.Date(string="Date", default=fields.Date.today)
    file = fields.Binary("Upload PDF")
    description = fields.Text("Description")
