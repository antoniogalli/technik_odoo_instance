odoo.define('pos_restaurant.floors', function (require) {
"use strict";

var PosBaseWidget = require('point_of_sale.BaseWidget');
var chrome = require('point_of_sale.chrome');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');

var QWeb = core.qweb;
var _t = core._t;


// EXTENDIENDO EL MODELO PARA CARGAR LA INFORMACION DE LA EMPRESA 'mobile','street'
models.load_models({
    model: 'res.company',
    fields: [ 'currency_id', 'email', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id' , 'country_id', 'state_id', 'tax_calculation_rounding_method','mobile','street'],
    loaded: function(self,companies){
        self.company = companies[0];
    },
});




//// EXTENDIENDO EL MODELO PARA CARGAR LA INFORMACION ADICIONAL DE LOS PRODUCTOS DE FARMACIA
//models.load_models(
//{
//        model:  'product.product',
//        fields: [ 'display_name','name', 'sequence', 'description',  'description_sale', 'type', 'rental', 'categ_id',
//         'list_price', 'volume', 'weight', 'sale_ok', 'purchase_ok', 'uom_id',
//         'company_id', 'active', 'color', 'default_code', 'can_image_1024_be_zoomed',
//          'has_configurable_attributes', 'message_main_attachment_id', 'create_uid',
//          'sale_delay',
//            'service_type',  'pe_code_osce', 'pe_price', 'require_plate', 'product_add_mode', 'can_be_expensed', 'produce_delay',
//            'rating_last_value',  'inventory_availability', 'available_threshold',
//             'product_brand_ept_id', 'landed_cost_ok',
//             'Health_register', 'pharmaceutical_composition', 'pharmaceutical_form', 'route', 'dosage', 'quantity_per_presentation', 'origin', 'batch', 'due_date', 'available_in_pos', 'to_weight', 'pos_categ_id' ],
//        order:  _.map(['sequence','default_code','name'], function (name) { return {name: name}; }),
//        domain: function(self){
//            var domain = ['&', '&', ['sale_ok','=',true],['available_in_pos','=',true],'|',['company_id','=',self.config.company_id[0]],['company_id','=',false]];
//            if (self.config.limit_categories &&  self.config.iface_available_categ_ids.length) {
//                domain.unshift('&');
//                domain.push(['pos_categ_id', 'in', self.config.iface_available_categ_ids]);
//            }
//            if (self.config.iface_tipproduct){
//              domain.unshift(['id', '=', self.config.tip_product_id[0]]);
//              domain.unshift('|');
//            }
//            return domain;
//        },
//        context: function(self){ return { display_default_code: false }; },
//        loaded: function(self, products){
//          console.log("Aqui el resultado XXX");
//            var exports = {};
//            var using_company_currency = self.config.currency_id[0] === self.company.currency_id[0];
//            var conversion_rate = self.currency.rate / self.company_currency.rate;
//            self.db.add_products(_.map(products, function (product) {
//                if (!using_company_currency) {
//                    product.lst_price = round_pr(product.lst_price * conversion_rate, self.currency.rounding);
//                }
//                product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
//                product.pos = self;
//                return new exports.Product({}, product);
//            }));
//        },
//    }
// );







// EXTENDIENDO EL MODELO PARA COLOCAR LA DIRECCION, EL NUMERO DE TELEFONO MOBIL Y EL PRIMER NOMBRE DEL CAJERO
var _super_order = models.Order.prototype;
models.Order = models.Order.extend({

    export_for_printing: function() {
        var json = _super_order.export_for_printing.apply(this,arguments);
        json.company.mobile=this.pos.company.mobile;
        json.company.street=this.pos.company.street;
        var nombrecortado = json.cashier.split(" ");
        var primernombre = nombrecortado[0];
        json.cashier_name=primernombre;

        var curr_client = this.pos.get_order().get_client();
        json.curr_client=curr_client;
//  console.log("Aqui el resultado XXX");
        return json;
    },
});




var _super_orderline = models.Orderline.prototype;

models.Orderline = models.Orderline.extend({

     export_for_printing: function() {
       var json = _super_orderline.export_for_printing.apply(this,arguments);
        var object_product_id =this.get_product();
         console.log(object_product_id);
        json.object_product_id=object_product_id;
        return json;
    },

    });




});