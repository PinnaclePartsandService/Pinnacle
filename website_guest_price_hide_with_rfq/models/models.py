# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Website(models.Model):
    _inherit = 'website'

    is_guest_user = fields.Boolean(string="Guest User hide price")
    guest_user_notice = fields.Char(string="Guest User Notice", translate=True)
    is_login_user = fields.Boolean(string="Login User hide price")
    login_user_notice = fields.Char(string="Login User Notice", translate=True)
    product_enable_rfq = fields.Boolean(string="Product RFQ")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_guest_user = fields.Boolean(
        string="Guest User hide price", related="website_id.is_guest_user", readonly=False)
    guest_user_notice = fields.Char(
        string="Guest User Notice", related="website_id.guest_user_notice", readonly=False, translate=True)
    is_login_user = fields.Boolean(
        string="Login User hide price", related="website_id.is_login_user", readonly=False)
    login_user_notice = fields.Char(
        string="Login User Notice", related="website_id.login_user_notice", readonly=False, translate=True)
    product_enable_rfq = fields.Boolean(
        string="Global Product RFQ", related="website_id.product_enable_rfq", readonly=False, translate=True)

    @api.constrains('is_guest_user', 'is_login_user')
    def _constrains_price_show(self):
        if self.is_guest_user and self.is_login_user:
            raise UserError(
                _('You can not use both option for hide website price'))

    # @api.onchange('product_enable_rfq')
    # def _onchange_product_enable_rfq(self):
    #     all_product = self.env['product.template'].search([])
    #     if self.product_enable_rfq:
    #         for rec in all_product:
    #             rec.enable_rfq = True
