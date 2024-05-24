# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.misc import xlwt

from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
import xlsxwriter

import io
from pytz import timezone
import pytz
import base64
from xlwt import easyxf


class kardex_productos_inventario(models.TransientModel):
    _name = "kardex.productos.mov"
    _description = "kardex productos"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(
            timezone(self.env.user.tz or "UTC")
        )

    @api.model
    def _get_from_date(self):
        company_id = self.env.user.company_id
        current_date = date.today()
        from_date = company_id.compute_fiscalyear_dates(current_date)["date_from"]
        return from_date

    excel_binary = fields.Binary("Field")
    all_products = fields.Boolean("¿Todos los productos?", default=False)
    file_name = fields.Char("Reporte Excel", readonly=True)
    product = fields.Many2one("product.product", string="Product")
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
        string="Compañía",
    )

    ubicacion = fields.Many2one(
        "stock.location", domain=[("usage", "=", "internal")], string="Ubicación"
    )

    date_from = fields.Date(string="Fecha desde", default=_get_from_date)
    date_to = fields.Date(string="Fecha hasta", default=fields.Date.today)
    revisio = fields.Char(string="Revisión")

    cantidad_inicial = fields.Float("Cant. inicial:", readonly=True)
    costo_promedio_inicial = fields.Float("Costo Inicial:", readonly=True)
    costo_total_inicial = fields.Float("Costo Total Ini:", readonly=True)

    cantidad_final = fields.Float("Cant. final:", readonly=True)
    costo_promedio = fields.Float("Costo final:", readonly=True)
    costo_total = fields.Float("Costo Total final", readonly=True)

    aplica = fields.Selection(
        [("todas", "Todos "), ("ubicacion", "Por ubicación")],
        required=True,
        default="todas",
        string="Selection location",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
        readonly=True,
    )

    obj_kardex = fields.One2many(
        comodel_name="kardex.productos.mov.detalle",
        inverse_name="obj_kardex_mostrarmovi",
    )

    def _action_imprimir_excel(
        self,
    ):

        workbook = xlwt.Workbook()
        column_heading_style = easyxf("font:height 200;font:bold True;")
        worksheet = workbook.add_sheet("Kardex")
        date_format = xlwt.XFStyle()
        date_format.num_format_str = "dd/mm/yyyy"

        number_format = xlwt.XFStyle()
        number_format.num_format_str = "#,##0.00"

        # Ponemos los primeros encabezados
        worksheet.write(0, 0, _("Reporte de Kardex"), column_heading_style)

        query_rorte = """
            select Max(id) as id  from kardex_productos_mov 
            """
        self.env.cr.execute(
            query_rorte,
        )
        tr = self.env.cr.dictfetchall()
        for tr_t in tr:
            todo_reporte = self.env["kardex.productos.mov"].search(
                [("id", "=", int(tr_t["id"]))]
            )
            tf = 0
            for todfact in todo_reporte:
                worksheet.write(1, 0, "Fecha desde:", column_heading_style)
                worksheet.write(1, 1, todfact.date_from, date_format)
                worksheet.write(2, 0, "Fecha hasta:", column_heading_style)
                worksheet.write(2, 1, todfact.date_to, date_format)

                worksheet.write(1, 2, "Producto:", column_heading_style)
                worksheet.write(1, 3, todfact.product.name)
                worksheet.write(2, 2, "Compañía:", column_heading_style)
                worksheet.write(2, 3, todfact.company_id.name)

                # Ponemos los primeros encabezados del detalle
        worksheet.write(4, 0, _("Fecha"), column_heading_style)
        worksheet.write(4, 1, _("RUC/DNI"), column_heading_style)
        worksheet.write(4, 2, _("Razón Social"), column_heading_style)
        worksheet.write(4, 3, _("Tipo"), column_heading_style)
        worksheet.write(4, 4, _("Guía"), column_heading_style)
        worksheet.write(4, 5, _("Documento"), column_heading_style)
        worksheet.write(4, 6, _("Cód Barras"), column_heading_style)
        worksheet.write(4, 7, _("Cód Producto"), column_heading_style)
        worksheet.write(4, 8, _("Producto"), column_heading_style)
        worksheet.write(4, 9, _("Unid. Medida"), column_heading_style)
        worksheet.write(4, 10, _("UdM SUNAT"), column_heading_style)
        worksheet.write(4, 11, _("Und. Entrada"), column_heading_style)
        worksheet.write(4, 12, _("Und. Salida"), column_heading_style)
        worksheet.write(4, 13, _("Und. Saldo"), column_heading_style)
        worksheet.write(4, 14, _("Costo Uni"), column_heading_style)
        worksheet.write(4, 15, _("Val. Entrada"), column_heading_style)
        worksheet.write(4, 16, _("Val. Salida"), column_heading_style)
        worksheet.write(4, 17, _("Saldo"), column_heading_style)
        worksheet.write(4, 18, _("Costo_Prom"), column_heading_style)
        worksheet.write(4, 19, _("Origen"), column_heading_style)
        worksheet.write(4, 20, _("Albaran"), column_heading_style)
        worksheet.write(4, 21, _("Inventario"), column_heading_style)

        heading = "Product Kardex Detail"
        # worksheet.write_merge(5, 0, 5,13, heading, easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
        # Se tiene que hacer de ultimo para saber cuanto mide todo

        # se recorre el reporte

        todo_reporte = self.env["kardex.productos.mov.detalle"].search(
            [("obj_kardex_mostrarmovi", "=", int(tr_t["id"]))]
        )
        tf = 0
        for todfact in todo_reporte:

            tf += 1
            ini = 4
            worksheet.write(tf + ini, 0, todfact.date, date_format)
            worksheet.write(tf + ini, 1, todfact.ruc_dni)
            worksheet.write(tf + ini, 2, todfact.razon_social)
            worksheet.write(tf + ini, 3, todfact.tipo)
            worksheet.write(tf + ini, 4, todfact.guia)
            worksheet.write(tf + ini, 5, todfact.documento)
            worksheet.write(tf + ini, 6, todfact.codigo_barras)
            worksheet.write(tf + ini, 7, todfact.codigo_producto)
            worksheet.write(tf + ini, 8, todfact.producto)
            worksheet.write(tf + ini, 9, todfact.unidad_medida)
            worksheet.write(tf + ini, 10, todfact.uom_sunat)
            worksheet.write(tf + ini, 11, todfact.u_entrada, number_format)
            worksheet.write(tf + ini, 12, todfact.u_salida, number_format)
            worksheet.write(tf + ini, 13, todfact.u_saldo, number_format)
            worksheet.write(tf + ini, 14, todfact.costo_unit, number_format)
            worksheet.write(tf + ini, 15, todfact.v_entrada, number_format)
            worksheet.write(tf + ini, 16, todfact.v_salida, number_format)
            worksheet.write(tf + ini, 17, todfact.v_saldo, number_format)
            worksheet.write(tf + ini, 18, todfact.costo_prom, number_format)
            worksheet.write(tf + ini, 19, todfact.origin, number_format)
            worksheet.write(tf + ini, 20, todfact.picking_id.name)
            worksheet.write(tf + ini, 21, todfact.inventario.name)

        fp = io.BytesIO()
        workbook.save(fp)
        excel_file = base64.encodestring(fp.getvalue())

        self.excel_binary = excel_file
        nombre_tabla = "Kardex Report.xls"
        self.file_name = nombre_tabla
        fp.close()

    # @api.depends('company')
    # def _actualizar_compania(self):
    #   self.company=domain=[('company_id', '=', self.company.id)]

    @api.onchange("company_id")
    def _cambio_company(self):
        #       # Set ubucacion ID
        if self.company_id:
            return {
                "domain": {
                    "ubicacion": [
                        ("company_id", "=", self.company_id.id),
                        ("usage", "=", "internal"),
                    ]
                }
            }

    # @api.one

    def _borracampos(self):
        self.cantidad_inicial = ""
        self.cantidad_final = ""
        self.costo_promedio = ""
        self.costo_total = ""
        self.aplica = "todas"
        self.company_id = ""

    def buscar_producto(self):
        if self.date_from > self.date_to:
            raise UserError(_("The Start date cannot be less than the end date "))
        else:
            self._borra_datos_tabla()

    def _borra_datos_tabla(self):
        query_rorte = """
            select Max(id) as id  from kardex_productos_mov 
            """
        self.env.cr.execute(
            query_rorte,
        )
        tr = self.env.cr.dictfetchall()
        for tr_t in tr:
            todo = self.env["kardex.productos.mov"].search(
                [("id", "<", int(tr_t["id"]))]
            )
            for tod in todo:
                tod.unlink()

            todo_reporte = self.env["kardex.productos.mov.detalle"].search(
                [("id", "<", int(tr_t["id"]))]
            )
            for tod in todo_reporte:

                tod.unlink()

        for karde in self:
            karde.obj_kardex.unlink()

        # Empezamos a realizar el saldo
        self._saldo_anterior()

    def _saldo_anterior(self, product_id=None):
        if self.all_products:
            query_total = self._moviento_completo_productos()
        else:
            query_total = self._moviento_completo()

        query_saldo_anterior = (
            """
            select (SUM(u_entrada)-SUM(u_salida))as u_ante , 
            (SUM(v_entrada)-SUM(v_salida))as v_ante  from (
            """
            + query_total
            + """
            ) as saldo_ante where date < %s --) este es para obtener el saldo anterior
            """
        )
        if product_id is None:
            producto = 0
            producto = self.product.id
        else:
            producto = product_id
        ubicacion = self.ubicacion.id
        date_from = self.date_from

        if self.all_products:
            if self.aplica == "todas":
                query_saldo_anterior_param = [date_from]

            if self.aplica == "ubicacion":
                query_saldo_anterior_param = [date_from]
        else:
            if self.aplica == "todas":
                query_saldo_anterior_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_from,
                )

            if self.aplica == "ubicacion":
                query_saldo_anterior_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_from,
                )

        self.env.cr.execute(query_saldo_anterior, query_saldo_anterior_param)

        saldo_anterior = self.env.cr.dictfetchall()
        for linea in saldo_anterior:
            self.cantidad_inicial = linea["u_ante"]
            self.costo_total_inicial = linea["v_ante"]
            if self.costo_total_inicial == 0:
                self.costo_promedio_inicial = 0
            if self.costo_total_inicial > 0:
                self.costo_promedio_inicial = (
                    self.costo_total_inicial / self.cantidad_inicial
                )

        # Ponemos el saldo anterior en la tabla
        self._saldo_anterior_tabla()

    def _saldo_anterior_tabla(self, product_id=None):
        for kardex in self:
            reference = "Balance previo"
            u_saldo = self.cantidad_inicial
            costo_uni = self.costo_promedio_inicial
            v_saldo = self.costo_total_inicial
            line = {
                "reference": reference,
                "u_saldo": u_saldo,
                "costo_unit": costo_uni,
                "v_saldo": v_saldo,
            }
            lines = [(0, 0, line)]
            kardex.write({"obj_kardex": lines})
        self._movimiento_producto()

    def _movimiento_producto(self, product_id=None):
        if self.all_products:
            query_total = self._moviento_completo_productos()
        else:
            query_total = self._moviento_completo()

        query_movimiento = (
            """
            select * from (
            """
            + query_total
            + """
            ) as mov where date >=%s and date <=%s 

            """
        )
        if product_id is None:
            producto = 0
            producto = self.product.id
        else:
            producto = product_id

        ubicacion = self.ubicacion.id
        date_from = self.date_from
        date_to = self.date_to

        if self.all_products:
            if self.aplica == "todas":
                query_movimiento_param = (
                    date_from,
                    date_to,
                )

            if self.aplica == "ubicacion":
                query_movimiento_param = (
                    date_from,
                    date_to,
                )
        else:
            if self.aplica == "todas":
                query_movimiento_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_from,
                    date_to,
                )

            if self.aplica == "ubicacion":
                query_movimiento_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_from,
                    date_to,
                )

        self.env.cr.execute(query_movimiento, query_movimiento_param)

        movim = self.env.cr.dictfetchall()
        for mov in movim:
            for kardex in self:
                fecha = mov["date"]
                ruc_dni = mov["ruc_dni"]
                razon_social = mov["razon_social"]
                tipo = mov["tipo"]
                guia = mov["guia"]
                documento = mov["documento"]
                codigo_barras = mov["codigo_barras"]
                codigo_producto = mov["codigo_producto"]
                producto = mov["producto"]
                unidad_medida = mov["unidad_medida"]
                uom_sunat = mov["uom_sunat"]
                picking_name = mov["picking_name"]
                sequence_code = mov["sequence_code"]
                u_entrada = mov["u_entrada"]
                u_salida = mov["u_salida"]
                u_saldo = mov["u_saldo"]
                costo_unit = mov["costo_unit"]
                v_entrada = mov["v_entrada"]
                v_salida = mov["v_salida"]
                v_saldo = mov["v_saldo"]
                origin = mov["origin"]
                reference = mov["reference"]
                picking_id = mov["picking_id"]
                inventario = mov["inventory_id"]

                line = {
                    "date": fecha,
                    "ruc_dni": ruc_dni,
                    "razon_social": razon_social,
                    "tipo": tipo,
                    "guia": guia,
                    "documento": documento,
                    "codigo_barras": codigo_barras,
                    "codigo_producto": codigo_producto,
                    "producto": producto,
                    "unidad_medida": unidad_medida,
                    "uom_sunat": uom_sunat,
                    "picking_name": picking_name,
                    "sequence_code": sequence_code,
                    "u_entrada": u_entrada,
                    "u_salida": u_salida,
                    "u_saldo": u_saldo,
                    "costo_unit": costo_unit,
                    "v_entrada": v_entrada,
                    "v_salida": v_salida,
                    "v_saldo": v_saldo,
                    "origin": origin,
                    "reference": reference,
                    "picking_id": picking_id,
                    "inventario": inventario,
                }
                lines = [(0, 0, line)]
                kardex.write({"obj_kardex": lines})

        self._saldo_final()

    def _saldo_final(self, product_id=None):
        if self.all_products:
            query_total = self._moviento_completo_productos()
        else:
            query_total = self._moviento_completo()

        query_saldo_final = (
            """
            select (SUM(u_entrada)-SUM(u_salida))as u_saldo , 
            (SUM(v_entrada)-SUM(v_salida))as v_saldo  from (
            """
            + query_total
            + """

            )as saldo_ante where date <= %s --) estes espara obteber el saldo final

            """
        )
        if product_id is None:
            producto = 0
            producto = self.product.id
        else:
            producto = product_id

        ubicacion = self.ubicacion.id
        date_to = self.date_to

        if self.all_products:
            if self.aplica == "todas":
                query_saldo_final_param = [date_to]

            if self.aplica == "ubicacion":
                query_saldo_final_param = [date_to]
        else:
            if self.aplica == "todas":
                query_saldo_final_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_to,
                )

            if self.aplica == "ubicacion":
                query_saldo_final_param = (
                    producto,
                    producto,
                    producto,
                    producto,
                    producto,
                    date_to,
                )

        self.env.cr.execute(query_saldo_final, query_saldo_final_param)

        saldo_final = self.env.cr.dictfetchall()
        for linea in saldo_final:

            self.cantidad_final = linea["u_saldo"]
            self.costo_total = linea["v_saldo"]
            if self.costo_total > 0:
                self.costo_promedio = self.costo_total / self.cantidad_final

        # buscamos las facturas
        self._buscar_factura()

    def _moviento_completo(self, product_id=None):
        local_des = ""
        location_id = ""
        if self.aplica == "todas":
            local_des = "sm.location_dest_id > 0"
            location_id = "sm.location_id > 0"
        if self.aplica == "ubicacion":
            local_des = "(sm.location_dest_id=%s or sm.location_dest_id=5)"
            location_id = "sm.location_id=%s"

        query_movimiento = """
            SELECT
                id                                                                                ,
                CAST(date_expected AS date)                                                       ,
                date_expected AS date                                                             ,
                ruc_dni                                                                           ,
                razon_social                                                                      ,
                tipo                                                                              ,
                guia                                                                              ,
                documento                                                                         ,
                codigo_barras                                                                     ,
                codigo_producto                                                                   ,
                producto                                                                          ,
                unidad_medida                                                                     ,
                uom_sunat                                                                         ,
                company_id                                                                        ,
                producto                                                                          ,
                u_entrada                                                                         ,
                u_salida                                                                          ,
                SUM(u_entrada-u_salida) over (order by kardex2.date_expected asc,id asc)as u_saldo,
                costo_unit                                                                        ,
                v_entrada                                                                         ,
                v_salida                                                                          ,
                SUM(v_entrada-v_salida)over (order by kardex2.date_expected asc,id asc)as v_saldo ,
                partner_id                                                                        ,
                origin                                                                            ,
                reference                                                                         ,
                picking_name                                                                      ,
                sequence_code                                                                     ,
                pe_guide_id                                                                       ,
                pe_is_eguide                                                                      ,
                quantity                                                                          ,
                costo_unit                                                                        ,
                price_subtotal                                                                    ,
                price_total                                                                       ,
                company_id                                                                        ,
                inventory_id                                                                      ,
                picking_id
            FROM
                (
                    SELECT *
                    FROM
                        (
                            --Entradas con Purchase Orders
                            SELECT
                                smo.id            ,
                                smo.date_expected ,
                                '' AS ruc_dni     ,
                                '' as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                   AS tipo           ,
                                ''                    AS guia           ,
                                ''                    AS documento      ,
                                pproduct.barcode      AS codigo_barras  ,
                                pproduct.default_code AS codigo_producto,
                                ptemplate.name        AS producto       ,
                                uom.name              as unidad_medida  ,
                                uom.sunat_code        AS uom_sunat      ,
                                0.0                   AS u_entrada      ,
                                0.0                   AS u_salida       ,
                                0.0                   AS v_entrada      ,
                                0.0                   AS v_salida       ,
                                0.0                   AS v_saldo        ,
                                0                     AS partner_id     ,
                                smo.name              AS origin         ,
                                smo.reference                           ,
                                'Inventory'     AS picking_name             ,
                                'SET'           AS sequence_code            ,
                                0               AS pe_guide_id              ,
                                false           AS pe_is_eguide             ,
                                smo.product_qty AS quantity                 ,
                                0.0             AS costo_unit               ,
                                0.0             AS price_subtotal           ,
                                0.0             AS price_total              ,
                                smo.company_id                              ,
                                smo.inventory_id                            ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id IS NULL
                                AND smo.product_id        = %s
                                AND smo.state             = 'done'
                        )
                        AS inventory_records
                    UNION
                    SELECT *
                    FROM
                        (
                            --Entradas con Purchase Orders
                            SELECT
                                smo.id                              ,
                                smo.date_expected                   ,
                                partner.vat          AS ruc_dni     ,
                                partner.display_name as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                                AS tipo           ,
                                spo.pe_guide_number                AS guia           ,
                                po.partner_ref                     as documento      ,
                                pproduct.barcode                   AS codigo_barras  ,
                                pproduct.default_code              AS codigo_producto,
                                ptemplate.name                     AS producto       ,
                                uom.name                           as unidad_medida  ,
                                uom.sunat_code                     AS uom_sunat      ,
                                smo.product_qty                    as u_entrada      ,
                                0                                  as u_salida       ,
                                (smo.product_qty * smo.price_unit) AS v_entrada      ,
                                0.0                                AS v_salida       ,
                                0.0                                AS v_saldo        ,
                                po.partner_id                                        ,
                                smo.origin                                           ,
                                smo.reference                                        ,
                                spot.name AS picking_name                            ,
                                spot.sequence_code                                   ,
                                spo.pe_guide_id                                      ,
                                spo.pe_is_eguide                                     ,
                                po.quantity                                          ,
                                po.price_unit AS costo_unit                          ,
                                po.price_subtotal                                    ,
                                po.price_total                                       ,
                                smo.company_id                                       ,
                                smo.inventory_id                                     ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.stock_picking_type AS spot
                                    ON
                                        smo.picking_type_id = spot.id
                                INNER JOIN
                                    public.stock_picking AS spo
                                    ON
                                        smo.picking_id = spo.id
                                INNER JOIN
                                    (
                                        SELECT
                                            p_order.name                       ,
                                            p_order.date_approve               ,
                                            p_order.partner_ref                ,
                                            p_order.partner_id                 ,
                                            a_orderline.product_qty as quantity,
                                            a_orderline.price_unit             ,
                                            a_orderline.price_subtotal         ,
                                            a_orderline.price_total
                                        FROM
                                            public.purchase_order AS p_order
                                            INNER JOIN
                                                public.purchase_order_line AS a_orderline
                                                ON
                                                    a_orderline.order_id = p_order.id
                                        WHERE
                                            a_orderline.product_id = %s
                                    )
                                    AS po
                                    ON
                                        smo.origin = po.name
                                INNER JOIN
                                    public.res_partner AS partner
                                    ON
                                        po.partner_id = partner.id
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id                = 1
                                AND smo.product_id                 = %s
                                AND smo.state                      = 'done'
                                AND smo.purchase_line_id IS NOT NULL
                        )
                        AS in_records
                    UNION
                    SELECT *
                    FROM
                        (
                            --Salidas con Sale Orders
                            SELECT
                                smo.id                              ,
                                smo.date_expected                   ,
                                partner.vat          AS ruc_dni     ,
                                partner.display_name as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                                AS tipo              ,
                                spo.pe_guide_number                AS guia              ,
                                am.name                            AS documento         ,
                                pproduct.barcode                   AS codigo_barras     ,
                                pproduct.default_code              AS codigo_producto   ,
                                ptemplate.name                     AS producto          ,
                                uom.name                           as unidad_medida     ,
                                uom.sunat_code                     AS uom_sunat         ,
                                0                                  as u_entrada         ,
                                smo.product_qty                    as u_salida          ,
                                (smo.product_qty * smo.price_unit) AS v_entrada         ,
                                (am.amount_total_signed )             v_salida          ,
                                0.0                                AS v_saldo           ,
                                so.partner_invoice_id              as partner_id        ,
                                smo.origin                                              ,
                                smo.reference                                           ,
                                spot.name AS picking_name                               ,
                                spot.sequence_code                                      ,
                                spo.pe_guide_id                                         ,
                                spo.pe_is_eguide                                        ,
                                am.quantity                                             ,
                                (am.amount_total_signed/smo.product_qty ) as costo_unit ,
                                am.price_subtotal                                       ,
                                am.price_total                                          ,
                                smo.company_id                                          ,
                                smo.inventory_id                                        ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.stock_picking_type AS spot
                                    ON
                                        smo.picking_type_id = spot.id
                                INNER JOIN
                                    public.stock_picking AS spo
                                    ON
                                        smo.picking_id = spo.id
                                INNER JOIN
                                    public.sale_order AS so
                                    ON
                                        smo.origin = so.name
                                INNER JOIN
                                    (
                                        SELECT
                                            a_move.name               ,
                                            a_move.date               ,
                                            a_move.type               ,
                                            a_move.invoice_origin     ,
                                            a_move.amount_total_signed,
                                            a_moveline.quantity       ,
                                            a_moveline.price_unit     ,
                                            a_moveline.discount       ,
                                            a_moveline.debit          ,
                                            a_moveline.credit         ,
                                            a_moveline.balance        ,
                                            a_moveline.price_subtotal ,
                                            a_moveline.price_total
                                        FROM
                                            public.account_move AS a_move
                                            INNER JOIN
                                                public.account_move_line AS a_moveline
                                                ON
                                                    a_moveline.move_id = a_move.id
                                        WHERE
                                            a_moveline.product_id = %s
                                    )
                                    AS am
                                    ON
                                        so.name = am.invoice_origin
                                INNER JOIN
                                    public.res_partner AS partner
                                    ON
                                        so.partner_invoice_id = partner.id
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id            = 2
                                AND smo.product_id             = %s
                                AND smo.state                  = 'done'
                                AND smo.sale_line_id IS NOT NULL
                        )
                        AS out_records
                )
                AS kardex2
            ORDER BY
                date_expected
            """
        return query_movimiento

    def _moviento_completo_productos(self):
        query_movimiento = """
            SELECT
                id                                                                                ,
                CAST(date_expected AS date)                                                       ,
                date_expected AS date                                                             ,
                ruc_dni                                                                           ,
                razon_social                                                                      ,
                tipo                                                                              ,
                guia                                                                              ,
                documento                                                                         ,
                codigo_barras                                                                     ,
                codigo_producto                                                                   ,
                producto                                                                          ,
                unidad_medida                                                                     ,
                uom_sunat                                                                         ,
                company_id                                                                        ,
                producto                                                                          ,
                u_entrada                                                                         ,
                u_salida                                                                          ,
                SUM(u_entrada-u_salida) over (order by kardex2.date_expected asc,id asc)as u_saldo,
                costo_unit                                                                        ,
                v_entrada                                                                         ,
                v_salida                                                                          ,
                SUM(v_entrada-v_salida)over (order by kardex2.date_expected asc,id asc)as v_saldo ,
                partner_id                                                                        ,
                origin                                                                            ,
                reference                                                                         ,
                picking_name                                                                      ,
                sequence_code                                                                     ,
                pe_guide_id                                                                       ,
                pe_is_eguide                                                                      ,
                quantity                                                                          ,
                costo_unit                                                                        ,
                price_subtotal                                                                    ,
                price_total                                                                       ,
                company_id                                                                        ,
                inventory_id                                                                      ,
                picking_id
            FROM
                (
                    SELECT *
                    FROM
                        (
                            --Entradas con Purchase Orders
                            SELECT
                                smo.id            ,
                                smo.date_expected ,
                                '' AS ruc_dni     ,
                                '' as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                   AS tipo           ,
                                ''                    AS guia           ,
                                smo.name              AS documento      ,
                                pproduct.barcode      AS codigo_barras  ,
                                pproduct.default_code AS codigo_producto,
                                ptemplate.name        AS producto       ,
                                uom.name              as unidad_medida  ,
                                uom.sunat_code        AS uom_sunat      ,
                                0.0                   AS u_entrada      ,
                                0.0                   AS u_salida       ,
                                0.0                   AS v_entrada      ,
                                0.0                   AS v_salida       ,
                                0.0                   AS v_saldo        ,
                                0                     AS partner_id     ,
                                smo.name              AS origin         ,
                                smo.reference                           ,
                                'Inventory'     AS picking_name             ,
                                'SET'           AS sequence_code            ,
                                0               AS pe_guide_id              ,
                                false           AS pe_is_eguide             ,
                                smo.product_qty AS quantity                 ,
                                0.0             AS costo_unit               ,
                                0.0             AS price_subtotal           ,
                                0.0             AS price_total              ,
                                smo.company_id                              ,
                                smo.inventory_id                            ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id IS NULL
                                --AND smo.product_id        = 842
                                AND smo.state = 'done'
                        )
                        AS inventory_records
                    UNION
                    SELECT *
                    FROM
                        (
                            --Entradas con Purchase Orders
                            SELECT
                                smo.id                              ,
                                smo.date_expected                   ,
                                partner.vat          AS ruc_dni     ,
                                partner.display_name as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                                AS tipo           ,
                                spo.pe_guide_number                AS guia           ,
                                po.partner_ref                     as documento      ,
                                pproduct.barcode                   AS codigo_barras  ,
                                pproduct.default_code              AS codigo_producto,
                                ptemplate.name                     AS producto       ,
                                uom.name                           as unidad_medida  ,
                                uom.sunat_code                     AS uom_sunat      ,
                                smo.product_qty                    as u_entrada      ,
                                0                                  as u_salida       ,
                                (smo.product_qty * smo.price_unit) AS v_entrada      ,
                                0.0                                AS v_salida       ,
                                0.0                                AS v_saldo        ,
                                po.partner_id                                        ,
                                smo.origin                                           ,
                                smo.reference                                        ,
                                spot.name AS picking_name                            ,
                                spot.sequence_code                                   ,
                                spo.pe_guide_id                                      ,
                                spo.pe_is_eguide                                     ,
                                po.quantity                                          ,
                                po.price_unit AS costo_unit                          ,
                                po.price_subtotal                                    ,
                                po.price_total                                       ,
                                smo.company_id                                       ,
                                smo.inventory_id                                     ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.stock_picking_type AS spot
                                    ON
                                        smo.picking_type_id = spot.id
                                INNER JOIN
                                    public.stock_picking AS spo
                                    ON
                                        smo.picking_id = spo.id
                                INNER JOIN
                                    (
                                        SELECT
                                            p_order.name                       ,
                                            p_order.date_approve               ,
                                            p_order.partner_ref                ,
                                            p_order.partner_id                 ,
                                            a_orderline.product_id             ,
                                            a_orderline.product_qty as quantity,
                                            a_orderline.price_unit             ,
                                            a_orderline.price_subtotal         ,
                                            a_orderline.price_total
                                        FROM
                                            public.purchase_order AS p_order
                                            INNER JOIN
                                                public.purchase_order_line AS a_orderline
                                                ON
                                                    a_orderline.order_id = p_order.id
                                        ORDER BY
                                            p_order.name
                                    )
                                    AS po
                                    ON
                                        smo.origin         = po.name
                                        AND smo.product_id = po.product_id
                                INNER JOIN
                                    public.res_partner AS partner
                                    ON
                                        po.partner_id = partner.id
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id                = 1
                                AND smo.state                      = 'done'
                                AND smo.purchase_line_id IS NOT NULL
                        )
                        AS in_records
                    UNION
                    SELECT *
                    FROM
                        (
                            --Salidas con Sale Orders
                            SELECT
                                smo.id                              ,
                                smo.date_expected                   ,
                                partner.vat          AS ruc_dni     ,
                                partner.display_name as razon_social,
                                CASE
                                    WHEN smo.picking_type_id IS NULL
                                        THEN 'inventario'
                                    WHEN smo.picking_type_id = 1
                                        THEN 'compra'
                                    WHEN smo.picking_type_id = 2
                                        THEN 'venta'
                                END                                AS tipo              ,
                                spo.pe_guide_number                AS guia              ,
                                am.name                            AS documento         ,
                                pproduct.barcode                   AS codigo_barras     ,
                                pproduct.default_code              AS codigo_producto   ,
                                ptemplate.name                     AS producto          ,
                                uom.name                           as unidad_medida     ,
                                uom.sunat_code                     AS uom_sunat         ,
                                0                                  as u_entrada         ,
                                smo.product_qty                    as u_salida          ,
                                (smo.product_qty * smo.price_unit) AS v_entrada         ,
                                (am.amount_total_signed )             v_salida          ,
                                0.0                                AS v_saldo           ,
                                so.partner_invoice_id              as partner_id        ,
                                smo.origin                                              ,
                                smo.reference                                           ,
                                spot.name AS picking_name                               ,
                                spot.sequence_code                                      ,
                                spo.pe_guide_id                                         ,
                                spo.pe_is_eguide                                        ,
                                am.quantity                                             ,
                                (am.amount_total_signed/smo.product_qty ) as costo_unit ,
                                am.price_subtotal                                       ,
                                am.price_total                                          ,
                                smo.company_id                                          ,
                                smo.inventory_id                                        ,
                                smo.picking_id
                            FROM
                                public.stock_move AS smo
                                INNER JOIN
                                    public.stock_picking_type AS spot
                                    ON
                                        smo.picking_type_id = spot.id
                                INNER JOIN
                                    public.stock_picking AS spo
                                    ON
                                        smo.picking_id = spo.id
                                INNER JOIN
                                    public.sale_order AS so
                                    ON
                                        smo.origin = so.name
                                INNER JOIN
                                    (
                                        SELECT
                                            a_move.name               ,
                                            a_move.date               ,
                                            a_move.type               ,
                                            a_move.invoice_origin     ,
                                            a_move.amount_total_signed,
                                            a_moveline.product_id     ,
                                            a_moveline.quantity       ,
                                            a_moveline.price_unit     ,
                                            a_moveline.discount       ,
                                            a_moveline.debit          ,
                                            a_moveline.credit         ,
                                            a_moveline.balance        ,
                                            a_moveline.price_subtotal ,
                                            a_moveline.price_total
                                        FROM
                                            public.account_move AS a_move
                                            INNER JOIN
                                                public.account_move_line AS a_moveline
                                                ON
                                                    a_moveline.move_id = a_move.id
                                    )
                                    AS am
                                    ON
                                        so.name            = am.invoice_origin
                                        AND smo.product_id = am.product_id
                                INNER JOIN
                                    public.res_partner AS partner
                                    ON
                                        so.partner_invoice_id = partner.id
                                INNER JOIN
                                    public.product_product AS pproduct
                                    ON
                                        smo.product_id = pproduct.id
                                INNER JOIN
                                    product_template AS ptemplate
                                    ON
                                        pproduct.product_tmpl_id = ptemplate.id
                                INNER JOIN
                                    public.uom_uom AS uom
                                    ON
                                        smo.product_uom = uom.id
                            WHERE
                                smo.picking_type_id            = 2
                                AND smo.state                  = 'done'
                                AND smo.sale_line_id IS NOT NULL
                        )
                        AS out_records
                )
                AS kardex2
            ORDER BY
                date_expected
            """
        return query_movimiento

    def _buscar_factura(self, product_id=None):
        for fact in self.obj_kardex:
            if fact.origin:
                query_origen = """
                    select Min(id) as id from account_move where invoice_origin = %s 
                    """
                query_origen_param = (fact.origin,)

                self.env.cr.execute(query_origen, query_origen_param)

                movim = self.env.cr.dictfetchall()
                for mov in movim:
                    # #  facturas=self.env['account.invoice'].search([('origin','=',fact.origin)])

                    fact.account_invoice = mov["id"]

        self._action_imprimir_excel()


class kardex_productos_inventario_detalle(models.TransientModel):
    _name = "kardex.productos.mov.detalle"
    _description = "kardex productos"

    obj_kardex_mostrarmovi = fields.Many2one("kardex.productos.mov")

    date = fields.Date(string="Fecha")
    ruc_dni = fields.Char(string="RUC/DNI")
    razon_social = fields.Char(string="Razon Social")
    tipo = fields.Char(string="Tipo Mov.")
    guia = fields.Char(string="Guía")
    documento = fields.Char(string="Documento")
    codigo_barras = fields.Char(string="Código de barras")
    codigo_producto = fields.Char(string="Código de producto")
    producto = fields.Char(string="Producto")
    unidad_medida = fields.Char(string="Unidad de medida")
    uom_sunat = fields.Char(string="Cod. UdM SUNAT")
    u_entrada = fields.Float()
    u_salida = fields.Float()
    u_saldo = fields.Float()
    costo_unit = fields.Float(string="Costo Unitario")
    v_entrada = fields.Float()
    v_salida = fields.Float()
    v_saldo = fields.Float()
    costo_prom = fields.Float()
    picking_name = fields.Char(string="Ref. Inventario")
    sequence_code = fields.Char()
    company_id = fields.Many2one("res.company", string="Compañia")
    state = fields.Char(string="Estado")
    reference = fields.Char(string="Referencia")
    origin = fields.Char(string="Origen")
    picking_id = fields.Many2one("stock.picking", string="Picking")
    account_invoice = fields.Many2one("account.move", string="Factura")
    inventario = fields.Many2one("stock.inventory", string="Inventario")
