odoo.define('website_guest_price_hide_with_rfq.hide_price', function(require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var qweb = core.qweb;

    ajax.loadXML('/website_guest_price_hide_with_rfq/static/src/xml/hide_product_price.xml', core.qweb);

    publicWidget.registry.productsSearchBar.include({
        _render: function (res) {
            var $prevMenu = this.$menu;
            this.$el.toggleClass('dropdown show', !!res);
            if (res) {
                var products = res['products'];
                this.$menu = $(qweb.render('website_sale.productsSearchBar.autocomplete', {
                    products: products,
                    hasMoreProducts: products.length < res['products_count'],
                    currency: res['currency'],
                    login: res['login'],
                    is_guest_user: res['is_guest_user'],
                    is_login_user: res['is_login_user'],
                    product_enable_rfq: res['product_enable_rfq'],
                    widget: this,
                }));
                this.$menu.css('min-width', this.autocompleteMinWidth);
                this.$el.append(this.$menu);
            }
            if ($prevMenu) {
                $prevMenu.remove();
            }
        },
    });

    publicWidget.registry.productsRecentlyViewedSnippet.include({
        _render: function (res) {
            var products = res['products'];
            var mobileProducts = [], webProducts = [], productsTemp = [];
            _.each(products, function (product) {
                if (productsTemp.length === 4) {
                    webProducts.push(productsTemp);
                    productsTemp = [];
                }
                productsTemp.push(product);
                mobileProducts.push([product]);
            });
            if (productsTemp.length) {
                webProducts.push(productsTemp);
            }
            this.mobileCarousel = $(qweb.render('website_sale.productsRecentlyViewed', {
                uniqueId: this.uniqueId,
                productFrame: 1,
                productsGroups: mobileProducts,
                login: res['login'],
                is_guest_user: res['is_guest_user'],
                is_login_user: res['is_login_user'],
                product_enable_rfq: res['product_enable_rfq'],
            }));
            this.webCarousel = $(qweb.render('website_sale.productsRecentlyViewed', {
                uniqueId: this.uniqueId,
                productFrame: 4,
                productsGroups: webProducts,
                login: res['login'],
                is_guest_user: res['is_guest_user'],
                is_login_user: res['is_login_user'],
                product_enable_rfq: res['product_enable_rfq'],
            }));
            this._addCarousel();
            this.$el.toggleClass('d-none', !(products && products.length));
        },
    });

    publicWidget.registry.WebsiteSale.include({
        _onChangeCombination: function (ev, $parent, combination){
            $('input[name=lead_product]').val(combination.product_id).trigger('input');
            $('input[name=name]').val(combination.display_name).trigger('input');
            this._super.apply(this, arguments);
        }
    });
});
