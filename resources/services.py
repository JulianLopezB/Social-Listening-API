import json
from flask_restful import Resource, reqparse
from resources.src.social_listening import SocialListening
from resources.src.fraud import FraudDetector

class SocialListeningService(Resource):
    def get(self):
        args = parser.parse_args()
        result = clf.predict(str(args["text"]))
        return result

class SentimentService(Resource):
    def get(self):
        args = parser.parse_args()
        result = clf.predict_sentiment(str(args["text"]))
        return result

class TagsService(Resource):
    def get(self):
        args = parser.parse_args()
        result = clf.predict_tags(str(args["text"]))
        return result

class AudienciasService(Resource):
    def get(self):
        args = parser.parse_args()
        result = clf.predict_audiencia(str(args["text"]))
        return result

class FraudService(Resource):
    def get(self):
        args = parser.parse_args()
        result = detector.detect(json.loads(args["user_info"]), str(args["source"]))
        return result


parser = reqparse.RequestParser()
parser.add_argument("text")
parser.add_argument("source")
parser.add_argument("user_info")

clf = SocialListening()
detector = FraudDetector()


