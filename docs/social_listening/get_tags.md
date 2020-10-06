# Tags

Obtiene las etiquetas asociadas a un comentario (texto libre) hecho por un usuario/cliente

**URL** : `/predict/`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

***Input***

`ejemplo = ["Hola, quisiera abrir una cuenta de ahorro con el Banco Galicia."]`

`parametros = {"text": ejemplo}`

***Output***

```json
{
    "tags": ["ProdServicios", "Cuentas", "SolicitudCliente", "Alta", "Cuenta"]
}
```
