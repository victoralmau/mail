Añade el campo de duration en mail.message y modifica el body para que SI permita HTML
Adicionalmente ANTES de envíar un mensaje a través de mail.compose.message comprueba si el tamaño de los adjuntos es >=10MB (debido a SES no se permite)
