# train and save model with given data

import numpy as np
from sklearn import preprocessing, linear_model
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from feature_extractor import generate_feature_data, generate_final_data
import pickle

# Directory path, file names for saved models
MODEL_DIR_PATH = './models'
LR_FILENAME = '/lr_model.sav'
KNN_FILENAME = '/knn_model.sav'
RANDOM_FOREST_FILENAME = '/rf_model.sav'
SVM_FILENAME = '/svm_model.sav'


X = np.load('input_data.npy')
y = np.load('output_data.npy')
(a, b, c) = X.shape
X = X.reshape(a, b*c)
X = preprocessing.normalize(X, axis=0)


# logistic regression
lr = linear_model.LogisticRegression(solver='saga')
lr_scores = cross_val_score(lr, X, y, cv=5)
lr.fit(X, y)
f = open(MODEL_DIR_PATH + LR_FILENAME, 'wb')
pickle.dump(lr, f)
f.close()
print (lr_scores)
print (np.mean(lr_scores))

# KNeighbors Classifier
knn = KNeighborsClassifier(n_neighbors=2)
knn_scores = cross_val_score(knn, X, y, cv=5)
knn.fit(X, y)
f = open(MODEL_DIR_PATH + KNN_FILENAME, 'wb')
pickle.dump(knn, f)
f.close()
print (knn_scores)
print (np.mean(knn_scores))

# Random Forest Classifier
max_value = -1
max_key = None
f = open(MODEL_DIR_PATH + RANDOM_FOREST_FILENAME, 'wb')
for i in range(10, 20):
     for j in range(10, 20):
         rand_forest = RandomForestClassifier(n_estimators=i, max_depth=j)
         rand_forest_scores = cross_val_score(rand_forest, X, y, cv=5)
        
         if (np.mean(rand_forest_scores) > max_value):
             max_value = np.mean(rand_forest_scores)
             max_key = (i, j)
             print (max_value)
             print (max_key)

         print (i, j)
(i, j) = max_key
rand_forest = RandomForestClassifier(n_estimators=i, max_depth=j)
rand_forest.fit(X,y)
pickle.dump(rand_forest, f)
f.close()
print (max_value, max_key)
print (rand_forest_scores)


# SVM Classifier
svm = SVC(gamma='auto')
svm_scores = cross_val_score(svm, X, y, cv=5)
svm.fit(X, y)
f = open(MODEL_DIR_PATH + SVM_FILENAME, 'wb')
pickle.dump(svm, f)
f.close()
print (svm_scores)
print (np.mean(svm_scores))
