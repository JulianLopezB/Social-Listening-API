# Audiencias

Obtiene audiencias asociadas al comentario (texto libre) hecho por un usuario/cliente

**URL** : `/predict/sentiment`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

***Input***

`ejemplo = "Me podrian pasar mas info por favor?"`

`parametros = {"text": ejemplo}`

***Output***

```json
{
    "audiencia": ["Promociones"]
}
```
