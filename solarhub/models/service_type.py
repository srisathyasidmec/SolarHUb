from odoo import models,fields,api


class SystemService(models.Model):
    _name="system.service"
    _description = "system service type"
    _rec_name = "title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")

