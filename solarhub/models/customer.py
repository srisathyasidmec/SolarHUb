from odoo import models,fields,api

class SolarCustomer(models.Model):
    _inherit="res.partner"

    company_id = fields.Many2one("res.company", string="Company")


    def send_email(self):
        for rec in self:
            template = self.env.ref("solarhub.mail_solar_customer_template")
            template.send_mail(rec.id, force_send=True)
    #
    # @api.onchange('complete_name')
    # def onchange_company(self):
    #     for rec in self:
    #         rec.company_id