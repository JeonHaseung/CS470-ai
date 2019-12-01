from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from sklearn import preprocessing
import pickle
from feature_extractor import extract_features
import numpy as np

TRAINING_INPUT_FILE_PATH = './input_data.npy'
MODEL_FILE_PATH = './models/rf_model.sav'

# f = open(MODEL_FILE_PATH, 'rb')
# model = pickle.load(MODEL_FILE_PATH)
# f.close()
with open(MODEL_FILE_PATH, 'rb') as pickle_file:
    model = pickle.load(pickle_file)


# load input_data to normalize text received
X = np.load('input_data.npy')

def extract_features_from_text(text):
    num_hashtag = len(text.split('#')) - 1
    feature_dict = extract_features(("", text, 0, 0, num_hashtag, ""))
    return [feature_dict['num_propagation_words'], feature_dict['text_length'], feature_dict['num_hashtag'], feature_dict['num_powerful_words'], feature_dict['num_personal_pronoun']]



text1 = input("text1: \n")
text2 = input("text2: \n")

print (text1)
print (text2)

feature_vector1 = extract_features_from_text(text1)
feature_vector2 = extract_features_from_text(text2)
print(feature_vector1)
print(feature_vector2)
input = np.array([[feature_vector1, feature_vector2]])
input = np.concatenate((X, input), axis=0)
print(input)            
(a, b, c) = input.shape
input = input.reshape(a, b*c)
print(input)             
input = preprocessing.normalize(input, axis=0)[-1]
print(input)             

result = model.predict([input])
print(result)
# 0: 1>2 / 1: 1<2
print ('result :'+ str(result[0]))
