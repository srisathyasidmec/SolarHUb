from odoo import models,fields,api


class SystemProperty(models.Model):
    _name="system.property"
    _description = "system property type"
    _rec_name = "title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")