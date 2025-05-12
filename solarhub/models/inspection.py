from odoo import models,fields,api


class SolarInspection(models.Model):
    _name='solar.inspection'
    _description='solar hub inspection'


    customer=fields.Many2one()
