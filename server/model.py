from konlpy.tag import Okt
from sklearn import linear_model, preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os
import csv


PROPAGATION_WORD_LIST = ['추천', '공유', '좋아요', '리트윗', '퍼뜨려', '퍼트려']
PERSONAL_PRONOUN_LIST = ['나', '내', '저', '제', '우리', '저희', '너', '네', '자네', '당신', '너희', '너희들', '자네들', '당신들', '니',
                         '니들', '그', '그이', '그들', '그이들', '그녀', '그녀들', '이', '저', '이들', '저들', '이분', '그분', '저분',
                         '누구', '누구들', '아무', '아무들', '걔', '걔들', '금마', '금마들', '임마', '임마들', '점마', '점마들',
                         '그자', '그자들', '그년', '그년들', '그놈', '그놈들', '저놈', '저놈들', '이놈', '이놈들', '이년', '이년들',
                         '저년', '저년들', '너놈', '너놈들', '너년', '너년들', '니놈', '니놈들', '니년', '니년들', '얘', '얘들',
                         '새기', '새기들', '샛기', '샛기들', '그새기', '그새기들', '이새기', '이새기들', '저새기', '저새기들',
                         '그샛기', '그샛기들', '이샛기', '이샛기들', '저샛기', '저샛기들', '새끼', '새끼들', '그새끼', '그새끼들',
                         '이새끼', '이새끼들', '저새끼', '저새끼들']
AGGRESSIVE_WORD_LIST = []

TAC_PAIRS_DIR_PATH = './tac_pairs'
AGGRESSIVE_WORDS_FILE_PATH = './real_good_words.txt'

def extract_features(row):
    # post_id, user_id, text, retweet, favorite, hashtag, create_time, url
    # 1. 공유를 직접적으로 의미하는 단어의 개수
    # 2. 글 길이
    # 3. 태그 개수
    # 4. 선정적이고 자극적인 단어
    # 5. 인칭대명사 개수

    # (post_id, user_id, text, num_retweet, num_favorite, num_hashtag, created_time, url) = row
    (user_id, text, num_retweet, num_favorite, num_hashtag, created_time) = row
    (num_propagation_words, text_length, num_personal_pronoun, num_aggressive_words) = (0, len(text), 0, 0)

    for i in PROPAGATION_WORD_LIST:
        num_propagation_words += len(text.split(i)) - 1

    for i in AGGRESSIVE_WORD_LIST:
        num_aggressive_words += len(text.split(i)) - 1

    for (morpheme, type) in Okt().pos(text):
        if type == 'Noun' and morpheme in PERSONAL_PRONOUN_LIST:
            num_personal_pronoun += 1

    feature_dict = {}
    feature_dict['num_propagation_words'] = int(num_propagation_words)
    feature_dict['text_length'] = int(text_length)
    feature_dict['num_hashtag'] = int(num_hashtag)
    feature_dict['num_aggressive_words'] = int(num_aggressive_words)
    feature_dict['num_personal_pronoun'] = int(num_personal_pronoun)
    feature_dict['num_retweet'] = int(num_retweet)

    return feature_dict



f = open(AGGRESSIVE_WORDS_FILE_PATH, 'r')
for word in f.readlines():
    AGGRESSIVE_WORD_LIST.append(word.strip())
f.close()

tac_pair_list = []

for file_name in os.listdir(TAC_PAIRS_DIR_PATH):
    file_path = TAC_PAIRS_DIR_PATH + '/' + file_name
    f = open(file_path, 'r')
    csv_reader = csv.reader(f)
    
    is_field_row = True
    data = []
    for row in csv_reader:
        if is_field_row:
            is_field_row = False
            continue

        feature_dict = extract_features(row)
        data.append(feature_dict)

    data_size = len(data)
    for i in range(0, data_size):
        for j in range(i+1, data_size):
            (data1, data2) = (data[i], data[j])
            if (data1['num_retweet'] + data2['num_retweet'] >= 10):
                tac_pair_list.append((data1, data2))

    f.close()

X = []
y = []
for tac_pair in tac_pair_list:
    (data1, data2) = tac_pair

    input_element = []

    for i in (data1, data2):
        input_element.append([
            i['num_propagation_words'],
            i['text_length'],
            i['num_hashtag'],
            i['num_aggressive_words'],
            i['num_personal_pronoun']
        ])
    X.append(input_element)

    if (data1['num_retweet'] > data2['num_retweet']):
        y.append(0)
    else:
        y.append(1)

X = np.array(X)
y = np.array(y)
print (np.shape(X))
print (np.shape(y))

np.save('input_data', X)
np.save('output_data', y)


# X = np.load('input_data.npy')
# y = np.load('output_data.npy')

# (a, b, c) = X.shape
# X = X.reshape(a, b*c)

# X = preprocessing.normalize(X, axis=0)

# #l1_logistic = linear_model.LogisticRegression(solver='saga')
# #l1_scores = cross_val_score(l1_logistic, X, y, cv=5)

# #knn = KNeighborsClassifier(n_neighbors=2)
# #knn_scores = cross_val_score(knn, X, y, cv=5)

# max_value = -1
# max_key = None
# for i in range(1, 20):
#     for j in range(1, 20):
#         rand_forest = RandomForestClassifier(n_estimators=i, max_depth=j)
#         rand_forest_scores = cross_val_score(rand_forest, X, y, cv=5)

#         if (np.mean(rand_forest_scores) > max_value):
#             max_value = np.mean(rand_forest_scores)
#             max_key = (i, j)
#             print (max_value)
#             print (max_key)

#         print (i, j)

# print (max_value, max_key)
