
import pickle
import pandas as pd
import logging as log
from flask import jsonify
from resources.paths import *
from resources.utils.helpers import *


import tensorflow.compat.v1 as tf
import tensorflow.compat.v1.keras.backend as K
import tensorflow.compat.v1.keras.models as models
from tensorflow.compat.v1 import Session, get_default_graph


''' ######### TF STUFF ########### '''

tf.disable_v2_behavior()
sess = Session()
graph = get_default_graph()
# IMPORTANT: models have to be loaded AFTER SETTING THE SESSION for keras!
# Otherwise, their weights will be unavailable in the threads after the session there has been set
K.set_session(sess)



class sentimentPredictor():


    with open(SENTIMENT_MODEL_PATH / 'tokenizer_sentiment.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

    model = models.load_model(SENTIMENT_MODEL_PATH / 'model_sentiment.h5',custom_objects={"f1_m": f1_m})

    def _init_(self):
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, text):

        clean_text = preProcess(text)
        seqs = self.tokenizer.texts_to_sequences([clean_text])
        seqs_oh = one_hot_seq(seqs)
        predicted_sentiment = self.model.predict(seqs_oh)[0]

        return predicted_sentiment

class tagPredictor():

    # Importo Tokenizer
    with open(TAGS_MODEL_PATH / 'tokenizer_tags.pkl', 'rb') as f:
        vect = pickle.load(f)

    def _init_(self):
        self.vect = vect


    def predict(self, text):

        list_tags  = pd.read_csv(TAGS_MODEL_PATH/ 'list_tags.csv')

        predicted_tags = []

        clean_text = [preProcess(x) for x in [text]]
        X_eval = self.vect.transform(clean_text)

        for label in list_tags['0'].tolist():

            pkl_filename = TAGS_CLS_PATH / str('model_{}.pkl'.format(label).strip())

            try:
                with open(pkl_filename, 'rb') as file:
                    pickle_model = pickle.load(file)
                predicted = pickle_model.predict(X_eval).tolist()
                predicted_tags.append([label if x == 1 else None for x in predicted])
            except:
                raise ValueError('No se pudo cargar el modelo {}'.format(pkl_filename))

        if predicted_tags:
            return [[x[s] for x in predicted_tags if x[s]!=None] for s in range(len(predicted_tags[0]))]
        else :
            return None


class audienciasClassifier():


    with open(AUDIENCIAS_MODEL_PATH / 'tokenizer_audiencias.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

    model = models.load_model(AUDIENCIAS_MODEL_PATH / 'model_audiencias.h5', custom_objects={"f1_m": f1_m})

    def _init_(self):
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, text):

        clean_text = preProcess(text)
        seqs = self.tokenizer.texts_to_sequences([clean_text])
        seqs_oh = one_hot_seq(seqs, nb_features=80000)
        predicted_audiencia = self.model.predict(seqs_oh)[0]

        return ['Promociones'] if predicted_audiencia.argmax()==1 else None




class SocialListening(object):

    def __init__(self):
        pass

    def predict(self, text):
        global sess
        global graph
        with graph.as_default():
            K.set_session(sess)
            try:
                sentiment_predictor = sentimentPredictor()
                tag_predictor = tagPredictor()
                sentiment_porcentual = sentiment_predictor.predict(text)
                sentiment = mapSentiment(sentiment_porcentual)
                tags = tag_predictor.predict(text)[0]

                prediction = {'sentiment_porcentual': str(sentiment_porcentual),
                            'sentiment': sentiment,
                            'tags': tags}

                return jsonify(prediction)

            except Exception as ex:
                print('Prediction Error')
                print(ex)

    def predict_sentiment(self, text):
        global sess
        global graph
        with graph.as_default():
            K.set_session(sess)
            try:
                sentiment_predictor = sentimentPredictor()
                sentiment_porcentual = sentiment_predictor.predict(text)
                sentiment = mapSentiment(sentiment_porcentual)

                prediction = {'sentiment_porcentual': str(sentiment_porcentual),
                            'sentiment': sentiment}

                return jsonify(prediction)

            except Exception as ex:
                log.log('Prediction Error', ex, ex.__traceback__.tb_lineno)
                print('Prediction Error')
                print(ex)


    def predict_tag(self, text):
        global sess
        global graph
        with graph.as_default():
            K.set_session(sess)
            try:
                predictor = tagPredictor()
                tags = predictor.predict(text)[0]
                prediction = {'tags': tags}

                return jsonify(prediction)

            except Exception as ex:
                log.log('Prediction Error', ex, ex.__traceback__.tb_lineno)
                print('Prediction Error')
                print(ex)


    def predict_audiencia(self, text):
        global sess
        global graph
        with graph.as_default():
            K.set_session(sess)
            try:
                audiencia_cassifier = audienciasClassifier()
                predicted_audiencia = audiencia_cassifier.predict(text)

                prediction = {'audiencia': predicted_audiencia}

                return jsonify(prediction)

            except Exception as ex:
                log.log('Prediction Error', ex, ex.__traceback__.tb_lineno)
                print('Prediction Error')
                print(ex)