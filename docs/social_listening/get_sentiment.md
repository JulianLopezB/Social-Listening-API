# Sentiment

Obtiene el sentimiento asociado a un comentario (texto libre) hecho por un usuario/cliente

**URL** : `/predict/sentiment`

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
    "sentiment": "Positivo"
}
```
