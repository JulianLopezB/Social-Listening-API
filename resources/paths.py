import os
import pathlib

''' ######### PATHS ######### '''

# Get the project directory as the parent of this module location
PATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent


DATA_PATH = PATH / 'data'

NLP_PATH = DATA_PATH / 'nlp_models'
SENTIMENT_MODEL_PATH = NLP_PATH/ 'sentiment'

TAGS_MODEL_PATH = NLP_PATH/ 'tags'
TAGS_CLS_PATH =TAGS_MODEL_PATH / 'classifiers'

AUDIENCIAS_MODEL_PATH = NLP_PATH/ 'audiencias'

FRAUD_PATH = DATA_PATH / 'fraude'
true_logo_path = FRAUD_PATH / 'true_logo.jpg'
perfiles_path =  FRAUD_PATH / 'perfiles_galicia.xlsx'