from odoo import models, fields, api

class Brand(models.Model):
    _name = 'solar.brand'
    _rec_name = 'brand_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    brand_name = fields.Char('Brand Name')