# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

import json
import requests

import logging
import sys
import traceback
# from datetime import datetime
import datetime

_logger = logging.getLogger(__name__)

url = 'https://service-it.com.ar'
username = 'api_user'
password = 'Segurament3Cu3n7asEl3gir'
subscripcion = ''
module_subs = 'subscription.subscription'
module_regist = 'sitinstanciasregistradas'
module_activ = 'sitinstanciasactivas'
modulos = ['account','stock','sale','purchase']

class mail_notification(models.Model):
    _name = 'mail_notification.mail_notification'
    _description = 'mail_notification.mail_notification'


    def daily_mail_notificacion(self):
        _logger.info("mail validation")


        erp_manager_group = self.env.ref('base.group_erp_manager')
        user_ids = self.env['res.users'].search([('groups_id', 'in', erp_manager_group.id)])
        usuarios_admin = user_ids.mapped('id')
        print("-->",usuarios_admin)


        usuario_admin = self.env['res.users'].search([('id','=',2)])
        contador_modulos = 0
        for modulo in modulos:
            existe_modulo = self.env['ir.module.module'].search([('name', '=', modulo), ('state', '=', 'installed')], limit=1).exists()    

            if existe_modulo:
                contador_modulos += 1

        if contador_modulos > 0:
            url_base = self.env['ir.config_parameter'].search([('key','=','web.base.url')])
            database_uuid = self.env['ir.config_parameter'].search([('key','=','database.uuid')])
            database_create_date = self.env['ir.config_parameter'].search([('key','=','database.create_date')])
            company = self.env['res.company'].search([('id','=',1)])
            query = "SELECT password from res_users where id = 2" 
            self._cr.execute(query)
            password_admin = self._cr.fetchall()
            instancia_local_id = database_uuid.value
            subscripcion = usuario_admin.partner_id.ref
            datos = {
                'usuarios_admin' : usuarios_admin,
                'usuario_admin' : usuario_admin.login,
                'password_admin' : password_admin,
                'empresa' : company.name,
                'url_odoo' : url_base.value,
                'database_uuid' : instancia_local_id,
                'database_create_date' : database_create_date.value,
                'subscripcion' : subscripcion
            }
            URL_REMOTO = 0
            try:
                r = requests.get(
                    url + '/api/auth/get_tokens',
                    headers = {'Content-Type': 'text/html; charset=utf-8'},
                    data = json.dumps({
                        'username': username,
                        'password': password,
                    }),
                )
                URL_REMOTO = 1

            except requests.exceptions.RequestException as e:
                if e.errno == 111:
                    print("Connection refused")

                fecha_creacion = datetime.datetime.strptime(database_create_date.value, "%Y-%m-%d %H:%M:%S")        
                dias_sin_registro = datetime.datetime.now() - fecha_creacion
                if dias_sin_registro > datetime.timedelta(days=7):
                    self.blocking()
            if not subscripcion:
                fecha_creacion = datetime.datetime.strptime(database_create_date.value, "%Y-%m-%d %H:%M:%S")        
                dias_sin_registro = datetime.datetime.now() - fecha_creacion
                if dias_sin_registro > datetime.timedelta(days=7):
                    self.blocking()
            else:                                    
                if URL_REMOTO == 1:
                    if r.status_code in [ 400, 401, 502]:
                        fecha_creacion = datetime.datetime.strptime(database_create_date.value, "%Y-%m-%d %H:%M:%S")        
                        dias_sin_registro = datetime.datetime.now() - fecha_creacion
                    else:

                        access_token = r.json()['access_token']

                        r2 = requests.get(
                            str(url) + "/api/" + str(module_subs) +"?filters=[('name','like','" + str(subscripcion) + "'),('active','=',True)]",
                            headers = {'Access-Token': access_token},
                        )


                        subscription_id=r2.json()['results'][0]['id']

                        r2 = requests.get(
                            str(url) + "/api/" + str(module_regist) +"?filters=[('subscription_id','like'," + str(subscription_id) + "),('name','like','" + str(instancia_local_id) + "')]",
                            headers = {'Access-Token': access_token},
                        )
                        if not r2.json()['results']:


                            r = requests.post(
                                url + '/api/' + str(module_regist),
                                headers = {
                                    'Content-Type': 'text/html; charset=utf-8',
                                    'Access-Token': access_token
                                },
                                data = json.dumps({
                                    'name':  str(instancia_local_id),
                                    'subscription_id':  subscription_id,
                                    'fecha_registrada': str(datetime.datetime.now()),
                                    'detalle_instancia': str(datos),
                                    'url': str(url_base.value),
                                    'sit_users_ids': str(usuarios_admin)

                                }),
                            )
                            print('Registered',r.text)


                        else: 

                            subscription_id=r2.json()['results'][0]['subscription_id']
                            instancias_activas=r2.json()['results'][0]['instancia_activa']



                            if instancias_activas:
                                r4 = requests.get(
                                    str(url) + "/api/" + str(module_activ) + "?filters=[('subscription_id','like','" + str(subscription_id) + "'),('name','like','" + str(instancia_local_id) + "')]",
                                    headers = {'Access-Token': access_token},
                                )
                                fecha_expiracion_str = r4.json()['results'][0]['fecha_expiracion']
                                
                                if fecha_expiracion_str:
                                    fecha_expiracion = datetime.datetime.strptime(fecha_expiracion_str, "%Y-%m-%d %H:%M:%S")        
                                    tiempo = fecha_expiracion - datetime.datetime.now()
                                    if tiempo > datetime.timedelta(0):
                                        print(str(datetime.datetime.now()) +  ", remain t ok")
                                        servidor_validado = True
                                        

                                        self.restoring(access_token,subscription_id,instancia_local_id)                    
                                    else:
                                        print(str(datetime.datetime.now()) +  ", no t remaining")
                                        self.blocking()

                                        servidor_validado = False
                                else:
                                    print(str(datetime.datetime.now()) +  ", all ok without remaining t")

                                    servidor_validado = True        # TO DO   OK
                                    self.restoring(access_token,subscription_id,instancia_local_id)

                            else:
                                print("Not act, wait 7d")
                                fecha_creacion = datetime.datetime.strptime(database_create_date.value, "%Y-%m-%d %H:%M:%S")        
                                dias_sin_registro = datetime.datetime.now() - fecha_creacion
                                if dias_sin_registro > datetime.timedelta(days=7):
                                    self.blocking()

                                else:
                                    print(str(datetime.datetime.now()) +  ",  days rem" + str(dias_sin_registro))
                                    self.restoring(access_token,subscription_id,instancia_local_id)


                    

    def send_message(self,MENSAJE):
        admin_users = self.env['res.users'].search([('groups_id', 'in', self.env.ref('base.group_system').id)])
        for admin  in admin_users:
            channel = self.env['mail.channel'].search([
                ('channel_partner_ids', 'in', [admin.partner_id.id]), 
                ('channel_partner_ids', 'in', [self.env.user.partner_id.id]), 
                ('channel_type', '=', 'chat')
            ], limit=1)

            if not channel:
                channel = self.env['mail.channel'].create({
                    'channel_partner_ids': [(6, 0, [admin.partner_id.id, self.env.user.partner_id.id])],
                    'channel_type': 'chat',
                    'name': 'Direct Message',
                })

            vals = {
                'subject': 'subject',
                'body': MENSAJE,
                'model': 'mail.channel',
                'res_id': channel.id,
                'message_type': 'comment',
                'subtype_id': self.env.ref('mail.mt_comment').id,
                'author_id': self.env.user.partner_id.id,
                'partner_ids': [(6, 0, [admin.partner_id.id, self.env.user.partner_id.id])],

            }
            enviando = self.env['mail.message'].create(vals)


            print(str(datetime.datetime.now()) + str(enviando))

            channel.message_post(
                body=MENSAJE,
                subject='subject',
                message_type='comment',
                subtype_id=self.env.ref('mail.mt_comment').id,
                author_id=self.env.user.partner_id.id,
                partner_ids=[admin.partner_id.id, self.env.user.partner_id.id]  # Enviar como lista de IDs

            )

    def  blocking(self):
        print("applying rules")

        erp_manager_group = self.env.ref('base.group_erp_manager')
        user_ids = self.env['res.users'].search([('groups_id', 'in', erp_manager_group.id)])
        sit_user_ids = user_ids.mapped('id')
        print("-->",sit_user_ids)

        user_id = 2
        admin_settings_group = self.env.ref('base.group_erp_manager')
        print("admin_settings_group=", admin_settings_group)

        for user_id in sit_user_ids:
            user = self.env['res.users'].browse(user_id)
            print("user=", user)
            if admin_settings_group in user.groups_id:
                resultado = user.sudo().write({'groups_id': [(3, admin_settings_group.id)]})
                delete_query = " DELETE FROM res_groups_users_rel WHERE uid = " + str(user_id) + " AND gid = " + str(admin_settings_group.id) + "; "
                self.env.cr.execute(delete_query)


                print("user.groups_id =", user.groups_id )
                print("result d =", resultado)
                





    def  restoring(self,access_token,subscription_id,instancia_local_id):
        import ast

        print("applying rules back")
        r2 = requests.get(
            str(url) + "/api/" + str(module_regist) +"?filters=[('subscription_id','like'," + str(subscription_id) + "),('name','like','" + str(instancia_local_id) + "')]",
            headers = {'Access-Token': access_token},
        )
        if not r2.json()['results']:
                print("Trying one instance")   #
        else:
            str_sit_users_ids =  r2.json()['results'][0]['sit_users_ids']
            sit_users_ids = ast.literal_eval(str_sit_users_ids)            


            for user_id in sit_users_ids:
                admin_settings_group = self.env.ref('base.group_erp_manager')
                user = self.env['res.users'].browse(user_id)
                print("user=", user)
                if admin_settings_group not in user.groups_id:
                    resultado= user.sudo().write({'groups_id': [(4, admin_settings_group.id)]})

                    print("user.groups_id =", user.groups_id )
                    print("result =", resultado)
                    
                    print("enabled to ID %s" % user_id)

