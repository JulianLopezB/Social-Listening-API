import os
import re
import emoji
import string
from unidecode import unidecode
from nltk.corpus import stopwords


stopwords = stopwords.words('spanish')
stopwords = [unidecode(x) for x in stopwords]
stopwords = [x for x in stopwords if x not in ['no', 'nunca', 'ningun', 'ninguna', 'ninguno', 'ni']]

punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
punc = punc + [x for x in string.punctuation if x not in punc]


def lemmatize(text):
    lemmatized = ' '.join([token.lemma_ for token in nlp(text)])
    return lemmatized

def removeStopwords(text):
    clean_text = ' '.join([word for word in text.split() if word.lower() not in stopwords])
    return clean_text


def addNegTag(text):
    clean_text = re.sub(r'\b(?:no|nunca|nada|ni|ningun|ninguno|ninguna|jamas|tampoco|pero|apenas|aunque|casi)\b[\w\s]+[^\w\s]',
    lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)),
    text, flags=re.IGNORECASE)
    return clean_text

def cleanPost(text):

    # remove mention
    clean_text = ' '.join(re.sub("(@[^\s]+)", "user_ref", str(text)).split())

    # remove hashtags
    clean_text = clean_text.replace('#','')

    # remove urls
    clean_text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '_url_ref_', clean_text)

    # remove punctuations
    #clean_text = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", clean_text).split())

    # emojis
    #clean_text = emoji.demojize(clean_text)
    #clean_text = clean_text.replace(":"," ")

    # mask emails
    clean_text = re.sub(r'\S*@\S*\s?', '_email_ref_', clean_text)

    # mask dates
    clean_text =  re.sub(r'(\d+/\d+/\d+)', '_date_ref_', clean_text)

    # mask time
    clean_text =  re.sub(r'^(?:(?:(\d+):)?(\d+):)?(\d+)$', '_time_ref_', clean_text)

    # remueve \n
    clean_text = clean_text.replace('\n', '')

    #remueve punctuations
    #clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))

    # mask numbers
    #clean_text =  re.sub(r'\d+', '_number_ref_', clean_text)

    #remueve tildes
    clean_text = unidecode(clean_text)

    #mask nombres
    #clean_text = ' '.join("_nombre_ref_" if word.lower() in list_names else word for word in clean_text.split())

    # lower case
    clean_text = clean_text.lower()

    # Replace multiple spaces by one space
    #clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text

def cleanText(text):
    ''' Remueve puntuaciones, tildes y otros simbolso

        Parameters
        ----------
        text: string libre

        Returns
        -------
        Texto limpio de caracteres no deseados
    '''
    clean_text = text.lower()

    # Remove punctuation marks
    punctuation = string.punctuation.replace('<', '').replace('>', '')
    replacePunctuation = str.maketrans(punctuation, ' '*len(punctuation))
    clean_text = clean_text.translate(replacePunctuation)

    # Remove accents
    clean_text = unidecode(clean_text)

    # Remove special remaining symbols
    clean_text = clean_text.translate ({ord(c): " "
                                        for c in "!@#$%^&*()[]{};:,./?\|`~-=_+"})

    return clean_text.lower().strip()
