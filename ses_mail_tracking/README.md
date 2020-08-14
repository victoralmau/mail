El módulo contiene el desarrollo relativo a hacer tracking de los emails a través de AWS SES

### odoo.conf
- aws_access_key_id=xxx
- aws_secret_key_id=xxxx
- aws_region_name=eu-west-1
- ses_sqs_url=https://sqs.eu-west-1.amazonaws.com/xxxx/exec_sns_ses

Se añade el campo de ses_state a la vista: mail_tracking.view_mail_tracking_email_form

Se crea un menú en Configuración > Técnico > SES > SES Mail Tracking con el listado de todos los datos.

Existe un cron Cron Check Ses Mail Tracking  que realiza la acción con cierta frecuencia para actualizar el estado del envío de cada email enviado desde Odoo.

### Cron Check Ses Mail Tracking

Frecuencia: 1 vez cada 30 min

Hora: 14:09

Descripción: Consulta los mensajes del SQS definido con el objetivo de guardar el estado del mismo y si procede (bounce o complaint) cambia el estado del envio del email en Odoo
