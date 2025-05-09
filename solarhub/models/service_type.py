from odoo import models,fields,api


class SystemService(models.Model):
    _name="system.service"
    _description = "system service type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")

