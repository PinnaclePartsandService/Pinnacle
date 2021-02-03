# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class RequestForm(http.Controller):

    @http.route('/shop/product/user_request_form', type='json', auth="public", methods=['POST'], website=True)
    def get_user_details(self, **kw):
        if kw:
            user_id = request.website.salesperson_id
            team_id = request.website.salesteam_id
            create_user_details_lead = request.env['crm.lead'].sudo().create({
                'name': kw.get('name'),
                'email_from': kw.get('email'),
                'description': kw.get('message'),
                'user_name': kw.get('username'),
                'lead_product_id': kw.get('product_id'),
                'phone': kw.get('phone'),
                'user_id': user_id.id if user_id else None,
                'team_id': team_id.id if team_id else None,
                'partner_id': request.env.user.partner_id.id if request.uid != request.website.user_id.id else None
            })
        return kw


class WebsiteSale(WebsiteSale):

    @http.route()
    def products_autocomplete(self, term, options={}, **kwargs):
        res = super(WebsiteSale, self).products_autocomplete(term, options, **kwargs)
        ProductTemplate = request.env['product.template']

        display_description = options.get('display_description', True)
        display_price = options.get('display_price', True)
        order = self._get_search_order(options)
        max_nb_chars = options.get('max_nb_chars', 999)

        category = options.get('category')
        attrib_values = options.get('attrib_values')

        domain = self._get_search_domain(term, category, attrib_values, display_description)
        products = ProductTemplate.search(
            domain,
            limit=min(20, options.get('limit', 5)),
            order=order
        )

        fields = ['id', 'name', 'website_url', 'enable_rfq']
        if display_description:
            fields.append('description_sale')
        if request.uid == request.website.user_id.id:
            login = False
        else:
            login = True

        res.update({
            'products': products.read(fields),
            'products_count': ProductTemplate.search_count(domain),
            'login': login,
            'is_guest_user': request.website.is_guest_user,
            'is_login_user': request.website.is_login_user,
            'product_enable_rfq': request.website.product_enable_rfq
        })

        if display_description:
            for res_product in res['products']:
                desc = res_product['description_sale']
                if desc and len(desc) > max_nb_chars:
                    res_product['description_sale'] = "%s..." % desc[:(max_nb_chars - 3)]

        if display_price:
            FieldMonetary = request.env['ir.qweb.field.monetary']
            monetary_options = {
                'display_currency': request.website.get_current_pricelist().currency_id,
            }
            for res_product, product in zip(res['products'], products):
                combination_info = product._get_combination_info(only_template=True)
                res_product.update(combination_info)
                res_product['list_price'] = FieldMonetary.value_to_html(res_product['list_price'], monetary_options)
                res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)

        return res

    def _get_products_recently_viewed(self):
        res = super(WebsiteSale, self)._get_products_recently_viewed()
        if request.uid == request.website.user_id.id:
            login = False
        else:
            login = True
        res.update({
            'login': login,
            'is_guest_user': request.website.is_guest_user,
            'is_login_user': request.website.is_login_user,
            'product_enable_rfq': request.website.product_enable_rfq,
            'products': [],
        })
        max_number_of_product_for_carousel = 12
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if visitor:
            excluded_products = request.website.sale_get_order().mapped('order_line.product_id.id')
            products = request.env['website.track'].sudo().read_group(
                [('visitor_id', '=', visitor.id), ('product_id', '!=', False), ('product_id.website_published', '=', True), ('product_id', 'not in', excluded_products)],
                ['product_id', 'visit_datetime:max'], ['product_id'], limit=max_number_of_product_for_carousel, orderby='visit_datetime DESC')
            products_ids = [product['product_id'][0] for product in products]
            if products_ids:
                viewed_products = request.env['product.product'].with_context(display_default_code=False).browse(products_ids)

                FieldMonetary = request.env['ir.qweb.field.monetary']
                monetary_options = {
                    'display_currency': request.website.get_current_pricelist().currency_id,
                }
                rating = request.website.viewref('website_sale.product_comment').active
                for product in viewed_products:
                    combination_info = product._get_combination_info_variant()
                    res_product = product.read(['id', 'name', 'website_url', 'enable_rfq'])[0]
                    res_product.update(combination_info)
                    res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)
                    if rating:
                        res_product['rating'] = request.env["ir.ui.view"]._render_template('portal_rating.rating_widget_stars_static', values={
                            'rating_avg': product.rating_avg,
                            'rating_count': product.rating_count,
                        })
                    res['products'].append(res_product)
        return res
