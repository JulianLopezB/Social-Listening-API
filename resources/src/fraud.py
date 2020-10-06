import cv2
import numpy as np
import pandas as pd
import logging as log
import urllib.request
from flask import jsonify

from resources.paths import *
from resources.utils.text_processing import cleanText


# Cargo los perfiles verdaderos y los convierto en diccionario
true_accounts = pd.read_excel(perfiles_path).groupby('social_network')['user'].apply(list).to_dict()

# todo pasar a lista csv
alert_words = ['.*bancogalicia',
              '.*banco.*galicia',
              '.*naranjax',
              '.*tarjeta.*naranja']



def searchWord(text):
    ''' Busca si un texto contiene una palabra en particular

        Parameters
        ----------
        text: string libre

        Returns
        -------
        Bool: True if contains a word in alert_words otherwise False
    '''
    text = cleanText(text)
    text = ".*" + ".*".join(text.split())
    return any([x in text for x in alert_words])

def isOfficialAccount(user_info, source):
    ''' Checks if user_info correspond to an official account

        Parameters
        ----------
        user_info: user info dictionary form facebook, instagram or twitter

        Returns
        -------
        True or False (bool)
    '''
    username = 'username' if source == 'Instagram' else 'screen_name' if source=='Twitter' else ''
    return user_info[username].lower() in [account.lower() for account in true_accounts[source]]

def createDetector():
    detector = cv2.ORB_create(nfeatures=2000)
    return detector

def getFeatures(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = cv2.ORB_create(nfeatures=2000)
    kps, descs = detector.detectAndCompute(gray, None)

    return kps, descs, img.shape[:2][::-1]


def detectFeatures(img, train_features, THRESHOLD):
    
    train_kps, train_descs, shape = train_features
    
    # get features from input image
    
    kps, descs, _ = getFeatures(img)
    
    # check if keypoints are extracted
    
    if not kps:
        return None
    
    # now we need to find matching keypoints in two sets of descriptors (from sample image, and from current image)
    # knnMatch uses k-nearest neighbors algorithm for that
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    
    matches = bf.knnMatch(train_descs, descs, k=2)
    
    good = []
    
    # apply ratio test to matches of each keypoint
    # idea is if train KP have a matching KP on image, it will be much closer than next closest non-matching KP,
    # otherwise, all KPs will be almost equally far
    
    for m, n in matches:
        
        if m.distance < THRESHOLD * n.distance:
            good.append([m])
            
    # stop if we didn't find enough matching keypoints
    if len(good) < 0.1 * len(train_kps):
        return None
    
    # estimate a transformation matrix which maps keypoints from train image coordinates to sample image
    src_pts = np.float32([train_kps[m[0].queryIdx].pt for m in good
                          ]).reshape(-1, 1, 2)
    
    dst_pts = np.float32([kps[m[0].trainIdx].pt for m in good
                          ]).reshape(-1, 1, 2)
    
    m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if m is not None:
        
        # apply perspective transform to train image corners to get a bounding box coordinates on a sample image
        scene_points = cv2.perspectiveTransform(np.float32([(0, 0), (0, shape[0] - 1), (shape[1] - 1, shape[0] - 1), (shape[1] - 1, 0)]).reshape(-1, 1, 2), m)
        rect = cv2.minAreaRect(scene_points)
        
        # check resulting rect ratio knowing we have almost square train image
        if rect[1][1] > 0 and 0.8 < (rect[1][0] / rect[1][1]) < 1.2:
            return rect
    return None


true_logo = cv2.imread(str(true_logo_path))
true_logo_gray = cv2.cvtColor(true_logo, cv2.COLOR_BGR2GRAY)
logo_features = getFeatures(true_logo)



# def has_galicia_logo(img_array):
#     # the 'Mean Squared Error' between the two images is the
#     # sum of the squared difference between the two images;
#     # NOTE: the two images must have the same dimension

#     pic_img = cv2.cvtColor(cv2.imdecode(img_array, -1), cv2.COLOR_BGR2GRAY) 
#     pic_img = cv2.resize(pic_img, true_logo_gray.shape, interpolation=cv2.INTER_CUBIC)

#     err = np.sum((true_logo_gray.astype("float") - pic_img.astype("float")) ** 2)
#     err /= float(true_logo_gray.shape[0] * true_logo_gray.shape[1])
#     if err < 1000:
#         return True

#     else:
#         return False


def hasGaliciaLogo(img_array):

    pic_img = cv2.imdecode(img_array, -1)

    region = detectFeatures(pic_img, logo_features, 0.8)

    if region:
        return True

    else:
        return False


def getColsSource(source):

    if source == 'Instagram':
        descriptive_cols = ['username', 'full_name','biography']
        pic_url = 'profile_pic_url'

    elif source == 'Twitter':
        descriptive_cols = ['name', 'screen_name','description']
        pic_url = 'profile_image_url_https'

    elif source == 'Facebook':
        descriptive_cols = None
        pic_url = None

    else:
        raise ValueError('''No se ha provisto red social correcta. Valores posibles: ,'''
                         +''' "Instagram", "Facebook", "Twitter" ''')

    return descriptive_cols, pic_url



def isFraud(user_info, source):
    ''' Detects if user is fraudulent

        Parameters
        ----------
        user_info: user info dictionary form facebook, instagram or twitter

        Returns
        -------
        True or False (bool)
    '''


    is_fraud_var = False
    description = None

    descriptive_cols, pic_url = getColsSource(source)


    if (not user_info) or isOfficialAccount(user_info, source):
        return (is_fraud_var, description)


    if descriptive_cols:

        message_cols =  "No se ha contado con informacion basica del usuario. "\
                        + "Proveer al menos una de estas categorias: "\
                        +f"{' ,'.join(col for col in descriptive_cols)}"

        # Corroboro que haya al menos una columna que pueda detectar fraude
        assert any(col in user_info.keys() for col in descriptive_cols), message_cols

        if any(searchWord(user_info[col]) for col in descriptive_cols
                           if type(col)==str):

            (is_fraud_var, description) = (True, 'description')

        else:

            if user_info[pic_url]:

                try:

                    url_response = urllib.request.urlopen(user_info[pic_url])
                    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

                    if hasGaliciaLogo(img_array):
                        (is_fraud_var, description) =  (True, 'image')

                except:
                    pass

        # if user_info[pic_url]:

        #     try:

        #         url_response = urllib.request.urlopen(user_info[pic_url])
        #         img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

        #         if hasGaliciaLogo(img_array):
        #             (is_fraud_var, description) =  (True, 'image')

        #     except:
        #         pass

           


    return (is_fraud_var, description)


class FraudDetector():

    def __init__(self):
        pass

    def detect(self, user_info, source):
        try:
            fraud = isFraud(user_info, source)
            prediction = {'is_fraud': fraud[0], 'match': fraud[1]}

            return jsonify(prediction)

        except Exception as ex:
            log.log('Prediction Error', ex, ex.__traceback__.tb_lineno)
            print('Prediction Error')
            print(ex)


