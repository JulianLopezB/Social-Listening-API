
import numpy as np
import tensorflow.compat.v1 as tf
import tensorflow.compat.v1.keras.backend as K
import tensorflow.compat.v1.keras.models as models
from tensorflow.compat.v1 import Session, get_default_graph
from resources.utils.text_processing import cleanPost, removeStopwords


''' ######### PARAMETROS ######### '''

NB_WORDS = 30000
SEQUENCE_LENGTH = 500



def one_hot_seq(seqs, nb_features = NB_WORDS):

    ohs = np.zeros((len(seqs), nb_features))
    for i, s in enumerate(seqs):
        ohs[i, s] = 1.
    return ohs

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())

    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())

    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)

    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def preProcess(text):
    if type(text) == str:
        clean_post = removeStopwords(text)
        #clean_post = text
        clean_post = cleanPost(clean_post)
        return clean_post

    else:
        return None

def mapSentiment(sentiment):
    if np.argmax(sentiment)==0:
        return 'Positivo'
    elif np.argmax(sentiment)==1:
        return 'Negativo'
    elif np.argmax(sentiment)==2:
        return 'Neutro'
    else:
        return None

