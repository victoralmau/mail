El módulo contienes el desarrollo para optimizar los destacados de los seguidores de los mensajes

Objetivo: Dejar destacados todos los mensajes para los comerciales de cualquier respuesta que se recibe con el objetivo de que no se "pierda" nada.

 

## mail.message (Mensajes)

Cuando hay contactos que necesitan acciones vinculadas con un mensaje:

Se recorren todos los partner_ids y aquellos que sean usuarios (comerciales) se lanza la acción generate_auto_starred_slack (https://github.com/OdooNodrizaTech/slack )

Se recorren todos los partner_ids y aquellos que sean usuarios (comerciales) se realiza un INSERT para dejar destacado ese mensaje

Cuando NO hay contactos que necesitan acciones vinculadas con un mensaje (respuestas de clientes por email):

Si el tipo de mensaje es un email, se buscan todos los seguidores del mensaje y para aquellos que sean usuarios (comerciales) se lanza la acción de generate_auto_starred_slack (https://github.com/OdooNodrizaTech/slack )

Si el tipo de mensaje es un emai, se buscan todos los seguidores del mensaje y para aquellos que sean usuarios (comerciales) se realiza un INSER para dejar destacado ese mensaje.

 

Para aquellos supuestos que cumplan las reglas anteriores (necesiten notificarse a un comercial) PERO por cualquier motivo no exista ningún comercial asociado a ese mensaje se lanza la acción de generate_notice_message_without_auto_starred_user_slack (https://github.com/OdooNodrizaTech/slack )
