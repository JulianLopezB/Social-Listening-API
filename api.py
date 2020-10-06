
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from resources.services import *



app = Flask(__name__)
api = Api(app)


# Social Listening
api.add_resource(SocialListeningService, '/predict')
api.add_resource(SentimentService, '/sentiment')
api.add_resource(TagsService, '/tags')
api.add_resource(AudienciasService, '/audiencias')

# Fraud
api.add_resource(FraudService, '/fraude')


if __name__=='__main__':

    try:
        app.run('localhost', port = 5000, debug = True, use_reloader = False)
    except Exception as e:
        print (e)


