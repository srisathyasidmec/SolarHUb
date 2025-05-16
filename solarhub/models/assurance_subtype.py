from odoo import models,fields,api


class SystemProperty(models.Model):
    _name="assurance.subtype"
    _description = "system assurance subtype"
    _rec_name = "assurance_subtype"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    assurance = fields.Many2one("system.assurance", "Assurance Type",required=True)
    assurance_subtype = fields.Char("Assurance SubType",required=True)
    unit_id = fields.Many2one("uom.uom","Unit")
    rate = fields.Float("Rate")