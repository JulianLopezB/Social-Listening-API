# Sentiment y Tags

Obtiene el sentimiento y las etiquetas asociados a un comentario (texto libre) hecho por un usuario/cliente

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
    "sentiment": "Positivo",
    "sentiment_porcentual": [9.8809296e-01 4.7369915e-04 1.1433230e-02],
    "tags": ["ProdServicios", "Cuentas", "SolicitudCliente", "Alta", "Cuenta"]
}
```
