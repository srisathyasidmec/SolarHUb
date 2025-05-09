from odoo import models,fields,api


class SystemProperty(models.Model):
    _name="system.assurance"
    _description = "system assurance type"
    _rec_name = "title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")