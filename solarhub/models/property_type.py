from odoo import models,fields,api


class SystemProperty(models.Model):
    _name="system.property"
    _description = "system property type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title=fields.Char("Title")