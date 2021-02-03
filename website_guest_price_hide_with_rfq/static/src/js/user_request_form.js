odoo.define('website_guest_price_hide_with_rfq.user_request_form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;


    publicWidget.registry.user_request_form = publicWidget.Widget.extend({
        selector: 'div[id$="product_details"]',
        events: {
            'submit #form_accept': 'submitForm',
        },
        submitForm: function(ev){
            var name = document.getElementById("name").value;
            var user_email = document.getElementById("email").value;
            var user_message = document.getElementById("message").value;
            var user_name = document.getElementById("username").value;
            var product_id = document.getElementById("product_id").value;
            var phone = document.getElementById("phone").value;
            
            if (name == ''){
                alert(' Product name required !');
                return false;
            }

            if (user_name == ''){
                alert(' Name required !');
                return false;
            }
            else if (user_email == ''){
                alert('Email required !');
                return false;
            }

            ev.preventDefault();
            this._rpc({
                route: "/shop/product/user_request_form",
                params: {
                    'name': name,
                    'email': user_email,
                    'username': user_name,
                    'message': user_message,
                    'product_id': product_id,
                    'phone': phone
                },
            }).then(function () {
                location.replace('')
            });
        },
    });
});
