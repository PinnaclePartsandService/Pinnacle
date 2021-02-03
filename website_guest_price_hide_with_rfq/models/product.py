# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    enable_rfq = fields.Boolean(string="Can be RFQ")


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_product_id = fields.Many2one('product.product', string="Product")
    user_name = fields.Char(string="User Name")

    @api.model
    def _onchange_user_values(self, user_id):
        """ returns new values when user_id has changed """
        if not user_id:
            return {}
        if user_id and self._context.get('team_id'):
            team = self.env['crm.team'].browse(self._context['team_id'])
            if user_id in team.member_ids.ids or user_id == team.user_id.id:
                return {}
        website = self.env['website'].get_current_website()
        if self.user_name:
            team_id = website.salesteam_id
            return {'team_id': team_id.id if team_id else None}
        team_id = self._default_team_id(user_id)
        return {'team_id': team_id}
