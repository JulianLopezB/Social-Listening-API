# Social-Listening API

## Uso

`python api.py`

## Test

`python tests/request.py`


## Endpoints

### Opinion Mining related

Cada endpoint devuelve un analisis diferente en relacion a un texto generado 
por un cliente o usuario

* [Sentiment y Tags](/docs/social_listening/get_all.md) : `GET /predict/`
* [Sentiment](/docs/social_listening/get_sentiment.md) : `GET /predict/sentiment`
* [Tags](/docs/social_listening/get_tags.md) : `GET /predict/tags`
* [Audiencias](/docs/social_listening/get_audiencias.md) : `GET /predict/audiencias`

### Fraud related

Unico endpoint que detecta si un perfil en redes sociales es falso

* [Detect Fraud](/docs/fraude/get_fraude.md) : `GET /fraud/`

