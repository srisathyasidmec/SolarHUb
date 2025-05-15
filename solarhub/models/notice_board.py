from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError,UserError


class SolarBattery(models.Model):
    _name = 'notice.board'
    _description = 'notice board'
    _rec_name="title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")
    date_today = fields.Date(string="Date", default=fields.Date.today)
    file = fields.Binary("Upload PDF")
    file_name = fields.Char("File Name")
    description = fields.Text("Description")

    @api.constrains('file_name')
    def _check_pdf_file_type(self):
        for rec in self:
            if rec.file_name and not rec.file_name.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are allowed.")
