from odoo import models, fields

class ProductProducts(models.Model):
    _inherit = "product.template"

    solarhub_type = fields.Selection(selection=[('solar panel','Solar Panel'),('battery','Battery'),('inverter','Inverter')], string="SolarHub Type")