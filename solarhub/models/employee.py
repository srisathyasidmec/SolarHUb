from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']