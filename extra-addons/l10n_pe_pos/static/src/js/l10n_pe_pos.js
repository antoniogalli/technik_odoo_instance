odoo.define('l10n_pe_pos.l10n_pe_pos', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PosDB = require('point_of_sale.DB');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    var _t = core._t;

    var PosModelSuper = models.PosModel;
    var OrderSuper = models.Order;

    function Unidades(num) {
        switch (num) {
            case 1: return "UN";
            case 2: return "DOS";
            case 3: return "TRES";
            case 4: return "CUATRO";
            case 5: return "CINCO";
            case 6: return "SEIS";
            case 7: return "SIETE";
            case 8: return "OCHO";
            case 9: return "NUEVE";
        }
        return "";
    }

    function Decenas(num) {
        var decena = Math.floor(num / 10);
        var unidad = num - (decena * 10);
        switch (decena) {
            case 1:
                switch (unidad) {
                    case 0: return "DIEZ";
                    case 1: return "ONCE";
                    case 2: return "DOCE";
                    case 3: return "TRECE";
                    case 4: return "CATORCE";
                    case 5: return "QUINCE";
                    default: return "DIECI" + Unidades(unidad);
                }
            case 2:
                switch (unidad) {
                    case 0: return "VEINTE";
                    default: return "VEINTI" + Unidades(unidad);
                }
            case 3: return DecenasY("TREINTA", unidad);
            case 4: return DecenasY("CUARENTA", unidad);
            case 5: return DecenasY("CINCUENTA", unidad);
            case 6: return DecenasY("SESENTA", unidad);
            case 7: return DecenasY("SETENTA", unidad);
            case 8: return DecenasY("OCHENTA", unidad);
            case 9: return DecenasY("NOVENTA", unidad);
            case 0: return Unidades(unidad);
        }
    }

    function DecenasY(strSin, numUnidades) {
        if (numUnidades > 0)
            return strSin + " Y " + Unidades(numUnidades)
        return strSin;
    }

    function Centenas(num) {
        var centenas = Math.floor(num / 100);
        var decenas = num - (centenas * 100);
        switch (centenas) {
            case 1:
                if (decenas > 0)
                    return "CIENTO " + Decenas(decenas);
                return "CIEN";
            case 2: return "DOSCIENTOS " + Decenas(decenas);
            case 3: return "TRESCIENTOS " + Decenas(decenas);
            case 4: return "CUATROCIENTOS " + Decenas(decenas);
            case 5: return "QUINIENTOS " + Decenas(decenas);
            case 6: return "SEISCIENTOS " + Decenas(decenas);
            case 7: return "SETECIENTOS " + Decenas(decenas);
            case 8: return "OCHOCIENTOS " + Decenas(decenas);
            case 9: return "NOVECIENTOS " + Decenas(decenas);
        }
        return Decenas(decenas);
    }

    function Seccion(num, divisor, strSingular, strPlural) {
        var cientos = Math.floor(num / divisor)
        var resto = num - (cientos * divisor)
        var letras = "";
        if (cientos > 0)
            if (cientos > 1)
                letras = Centenas(cientos) + " " + strPlural;
            else
                letras = strSingular;
        if (resto > 0)
            letras += "";
        return letras;
    }

    function Miles(num) {
        var divisor = 1000;
        var cientos = Math.floor(num / divisor)
        var resto = num - (cientos * divisor)
        var strMiles = Seccion(num, divisor, "UN MIL", "MIL");
        var strCentenas = Centenas(resto);
        if (strMiles == "")
            return strCentenas;
        return strMiles + " " + strCentenas;
    }

    function Millones(num) {
        var divisor = 1000000;
        var cientos = Math.floor(num / divisor)
        var resto = num - (cientos * divisor)
        var strMillones = Seccion(num, divisor, "UN MILLON DE", "MILLONES DE");
        var strMiles = Miles(resto);
        if (strMillones == "")
            return strMiles;
        return strMillones + " " + strMiles;
    }

    function numeroALetras(num, curData) {
        var data = {
            numero: num,
            enteros: Math.floor(num),
            centavos: (((Math.round(num * 100)) - (Math.floor(num) * 100))),
            letrasCentavos: "",
            letrasMonedaPlural: curData.plural,
            letrasMonedaSingular: curData.singular,
            letrasMonedaCentavoPlural: curData.centPlural,
            letrasMonedaCentavoSingular: curData.centSingular
        };

        if (data.centavos > 0) {
            data.letrasCentavos = "CON " + (function () {
                if (data.centavos == 1)
                    return Millones(data.centavos) + " " + data.letrasMonedaCentavoSingular;
                else
                    return Millones(data.centavos) + " " + data.letrasMonedaCentavoPlural;
            })();
        };

        if (data.enteros == 0)
            return "CERO " + data.letrasMonedaPlural + " " + data.letrasCentavos;
        if (data.enteros == 1)
            return Millones(data.enteros) + " " + data.letrasMonedaSingular + " " + data.letrasCentavos;
        else
            return Millones(data.enteros) + " " + data.letrasMonedaPlural + " " + data.letrasCentavos;
    }

    models.load_fields("res.currency", ["singular_name", "plural_name", "fraction_name", "show_fraction"]);
    models.load_fields("res.partner", [
        "doc_type", "doc_number", "commercial_name",
        "legal_name", "is_validate", "state", "condition",
        "l10n_latam_identification_type_id"]);

    models.load_models([{
        model: 'l10n_latam.identification.type',
        fields: ["name", "id", "l10n_pe_vat_code"],
        //domain: function(self){return [['country_id.code', '=', 'PE']]},
        loaded: function (self, identifications) {
            self.doc_code_by_id = {}
            _.each(identifications, function (doc) {
                self.doc_code_by_id[doc.id] = doc.l10n_pe_vat_code
            })
            self.doc_types = identifications
        },

    }])

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var res = PosModelSuper.prototype.initialize.apply(this, arguments);
            this.doc_types = []
            //~ {'code': '0', 'name':'DOC.TRIB.NO.DOM.SIN.RUC'},
            //~ {'code': '1', 'name':'DNI'},
            //~ {'code': '4', 'name':'CARNET DE EXTRANJERIA'},
            //~ {'code': '6', 'name':'RUC'},
            //~ {'code': '7', 'name':'PASAPORTE'},
            //~ {'code': 'A', 'name':'CÉDULA DIPLOMÁTICA DE IDENTIDAD'}];
            this.partner_states = [
                { 'code': 'ACTIVO', 'name': 'ACTIVO' },
                { 'code': 'BAJA DE OFICIO', 'name': 'BAJA DE OFICIO' },
                { 'code': 'BAJA PROVISIONAL', 'name': 'BAJA PROVISIONAL' },
                { 'code': 'SUSPENSION TEMPORAL', 'name': 'SUSPENSION TEMPORAL' },
                { 'code': 'INHABILITADO-VENT.UN', 'name': 'INHABILITADO-VENT.UN' },
                { 'code': 'BAJA MULT.INSCR. Y O', 'name': 'BAJA MULT.INSCR. Y O' },
                { 'code': 'PENDIENTE DE INI. DE', 'name': 'PENDIENTE DE INI. DE' },
                { 'code': 'OTROS OBLIGADOS', 'name': 'OTROS OBLIGADOS' },
                { 'code': 'NUM. INTERNO IDENTIF', 'name': 'NUM. INTERNO IDENTIF' },
                { 'code': 'ANUL.PROVI.-ACTO ILI', 'name': 'ANUL.PROVI.-ACTO ILI' },
                { 'code': 'ANULACION - ACTO ILI', 'name': 'ANULACION - ACTO ILI' },
                { 'code': 'BAJA PROV. POR OFICI', 'name': 'BAJA PROV. POR OFICI' },
                { 'code': 'ANULACION - ERROR SU', 'name': 'ANULACION - ERROR SU' },
            ];
            this.partner_conditions = [
                { 'code': 'HABIDO', 'name': 'HABIDO' },
                { 'code': 'NO HALLADO', 'name': 'NO HALLADO' },
                { 'code': 'NO HABIDO', 'name': 'NO HABIDO' },
                { 'code': 'PENDIENTE', 'name': 'PENDIENTE' },
                { 'code': 'NO HALLADO SE MUDO D', 'name': 'NO HALLADO SE MUDO D' },
                { 'code': 'NO HALLADO NO EXISTE', 'name': 'NO HALLADO NO EXISTE' },
                { 'code': 'NO HALLADO FALLECIO', 'name': 'NO HALLADO FALLECIO' },
                { 'code': 'NO HALLADO OTROS MOT', 'name': 'NO HALLADO OTROS MOT' },
                { 'code': 'NO APLICABLE', 'name': 'NO APLICABLE' },
                { 'code': 'NO HALLADO NRO.PUERT', 'name': 'NO HALLADO NRO.PUERT' },
                { 'code': 'NO HALLADO CERRADO', 'name': 'NO HALLADO CERRADO' },
                { 'code': 'POR VERIFICAR', 'name': 'POR VERIFICAR' },
                { 'code': 'NO HALLADO DESTINATA', 'name': 'NO HALLADO DESTINATA' },
                { 'code': 'NO HALLADO RECHAZADO', 'name': 'NO HALLADO RECHAZADO' },
                { 'code': '-', 'name': 'NO HABIDO' },
            ];
            return res;
        },
        validate_pe_doc: function (doc_type, doc_number) {
            if (!doc_type || !doc_number) {
                return false;
            }
            if (doc_number.length == 8 && doc_type == '1') {
                return true;
            }
            else if (doc_number.length == 11 && doc_type == '6') {
                var vat = doc_number;
                var factor = '5432765432';
                var sum = 0;
                var dig_check = false;
                if (vat.length != 11) {
                    return false;
                }
                try {
                    parseInt(vat)
                }
                catch (err) {
                    return false;
                }

                for (var i = 0; i < factor.length; i++) {
                    sum += parseInt(factor[i]) * parseInt(vat[i]);
                }

                var subtraction = 11 - (sum % 11);
                if (subtraction == 10) {
                    dig_check = 0;
                }
                else if (subtraction == 11) {
                    dig_check = 1;
                }
                else {
                    dig_check = subtraction;
                }

                if (parseInt(vat[10]) != dig_check) {
                    return false;
                }
                return true;
            }
            else if (doc_number.length >= 3 && ['0', '4', '7', 'A'].indexOf(doc_type) != -1) {
                return true;
            }
            else if (doc_type.length >= 2) {
                return true;
            }
            else {
                return false;
            }
        },
    });

    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            OrderSuper.prototype.initialize.apply(this, arguments);
        },
        get_doc_type: function () {
            var client = this.get_client();
            var doc_type = client ? client.doc_type : "";
            return doc_type;
        },
        get_doc_number: function () {
            var client = this.get_client();
            var doc_number = client ? client.doc_number : "";
            return doc_number;
        },
        get_amount_text: function () {
            return numeroALetras(this.get_total_with_tax(), {
                plural: this.pos.currency.plural_name,
                singular: this.pos.currency.singular_name,
                centPlural: this.pos.currency.show_fraction ? this.pos.currency.sfraction_name : "",
                centSingular: this.pos.currency.show_fraction ? this.pos.currency.sfraction_name : ""
            })
        },
    });

    screens.PaymentScreenWidget.include({

        order_is_valid: function (force_validation) {
            var res = this._super(force_validation);
            return res;
        },
        validate_journal_invoice: function () {
            var res = this._super()
            var order = this.pos.get_order();
            if (res) {
                return res;
            }
            if (!order.get_sale_journal()) {
                this.gui.show_popup('error', _t('It is required to Select a Journal'));
                res = true;
            }
            return res;
        },
    });

    screens.ClientListScreenWidget.include({
        display_client_details: function (visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);
            var self = this;
            var contents = this.$('.client-details-contents');
            if (contents.find("[name='doc_type']").val() == 6) {
                contents.find('.partner-state').show();
                contents.find('.partner-condition').show();
            }
            else {
                contents.find('.partner-state').hide();
                contents.find('.partner-condition').hide();
            }
            contents.find('.doc_number').on('change', function (event) {
                var doc_type = contents.find("[name='l10n_latam_identification_type_id']").val();
                doc_type = self.pos.doc_code_by_id[doc_type];
                var doc_number = this.value;
                self.set_client_details(doc_type, doc_number, contents);
            });
            contents.find("[name='l10n_latam_identification_type_id']").on('change', function (event) {
                var doc_type = self.pos.doc_code_by_id[this.value];
                var doc_number = contents.find(".doc_number").val();
                if (doc_type == "6") {
                    contents.find('.partner-state').show();
                    contents.find('.partner-condition').show();
                }
                else {
                    contents.find('.partner-state').hide();
                    contents.find('.partner-condition').hide();
                }
                if (doc_number && doc_type) {
                    self.set_client_details(doc_type, doc_number, contents);
                }
            });

        },
        set_client_details: function (doc_type, doc_number, contents) {
            var self = this;
            if (doc_type && !doc_number && doc_type != "0") {
                self.gui.show_popup('error', _t('El número de documento es obligatorio.'));
                return;
            }
            if (!doc_type && doc_number) {
                self.gui.show_popup('error', _t('El tipo de documento es obligatorio'));
                return;
            }
            if (doc_type && doc_number) {
                if (doc_type == "1" || doc_type == "6") {
                    if (!self.pos.validate_pe_doc(doc_type, doc_number)) {
                        self.gui.show_popup('error', {
                            'title': _t("Error en el Número de Documento"),
                            'body': _t("Por favor verificar que el tipo y/o número de documento del Cliente "),
                        });
                        return;
                    }
                    else {
                        rpc.query({
                            model: 'res.partner',
                            method: 'get_partner_from_ui',
                            args: [doc_type, doc_number],
                        }, {
                            timeout: 7500,
                        })
                            .then(function (result) {
                                if (result.detail != "Not found.") {
                                    if (doc_type == "1") {
                                        contents.find("[name='name']").val(result.name + ' ' + result.paternal_surname + ' ' + result.maternal_surname);
                                        contents.find('.vat').val(doc_number);
                                        contents.find('.is_validate').val(true);//attr('checked', true);
                                        contents.find('.last_update').val(result.last_update);
                                        contents.find('.doc_type').val(doc_type);
                                    }
                                    else if (doc_type == "6") {
                                        contents.find("[name='name']").val(result.legal_name);
                                        contents.find('.commercial_name').val(result.commercial_name);
                                        contents.find('.legal_name').val(result.legal_name);
                                        contents.find("[name='street']").val(result.street);
                                        contents.find('.is_validate').val(true);//attr('checked', true);
                                        contents.find('.vat').val(doc_number);
                                        contents.find('.last_update').val(result.last_update);
                                        contents.find("[name='state']").val(result.state);
                                        contents.find("[name='condition']").val(result.condition);
                                        contents.find("[name='doc_type']").val(doc_type);
                                    }
                                }
                            }).catch(function (type, error) {
                                console.error('Failed to get partner:');
                            });
                    }
                }
            }
        },
    });

});
