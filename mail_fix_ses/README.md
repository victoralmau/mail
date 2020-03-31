Motivo: Odoo al leer un email de un servidor de correo entrante (comercial.todocesped@gmail.com) intenta enviar el email tal cual lo lee, y al ser el remitente: emaildecliente NO puede enviar ese email a través de Amazon SES ya que SOLO están verificados los emails de los comerciales, por ello se cambia el remitente para que Odoo grabe la respuesta de ese email aunque luego no lo reciba de nuevo el comercial.


## Crones

### Mail Fix SES Exceptions 554

Frecuencia: cada 15 minutos

Hora: 09:07

Descripción: Revisa todos los emails que se han intentado enviar y tienen el estado 'Excepcion', de estos, se revisa si la razon de que fallen es ""Message rejected: Email address is not verified"" para en ese caso, colocar como "remitente" del mensaje (erp@oniad.com) e intenta evitarlo de nuevo

Motivo: Odoo al leer un email de un servidor de correo entrante (comercial.oniad@gmail.com) intenta enviar el email tal cual lo lee, y al ser el remitente: emaildecliente NO puede enviar ese email a través de Amazon SES ya que SOLO están verificados los emails de los comerciales, por ello se cambia el remitente para que Odoo grabe la respuesta de ese email aunque luego no lo reciba de nuevo el comercial.
