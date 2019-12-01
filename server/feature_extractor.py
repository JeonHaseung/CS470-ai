# This python file contains functions that generate feature data pairs from TAC pairs
from konlpy.tag import Okt
import numpy as np
import os, csv

# Propagation, personal pronoun words list.
PROPAGATION_WORD_LIST = ['추천', '공유', '좋아요', '리트윗', '퍼뜨려', '퍼트려']
PERSONAL_PRONOUN_LIST = ['나', '내', '저', '제', '우리', '저희', '너', '네', '자네', '당신', '너희', '너희들', '자네들', '당신들', '니',
                         '니들', '그', '그이', '그들', '그이들', '그녀', '그녀들', '이', '저', '이들', '저들', '이분', '그분', '저분',
                         '누구', '누구들', '아무', '아무들', '걔', '걔들', '금마', '금마들', '임마', '임마들', '점마', '점마들',
                         '그자', '그자들', '그년', '그년들', '그놈', '그놈들', '저놈', '저놈들', '이놈', '이놈들', '이년', '이년들',
                         '저년', '저년들', '너놈', '너놈들', '너년', '너년들', '니놈', '니놈들', '니년', '니년들', '얘', '얘들',
                         '새기', '새기들', '샛기', '샛기들', '그새기', '그새기들', '이새기', '이새기들', '저새기', '저새기들',
                         '그샛기', '그샛기들', '이샛기', '이샛기들', '저샛기', '저샛기들', '새끼', '새끼들', '그새끼', '그새끼들',
                         '이새끼', '이새끼들', '저새끼', '저새끼들']
# Powerful word is generated based on twitter messages and is saved on ./real_good_words.txt
POWERFUL_WORD_LIST = []
POWERFUL_WORDS_FILE_PATH = './real_good_words.txt'
f = open(POWERFUL_WORDS_FILE_PATH, 'r', encoding='UTF8')
for word in f.readlines():
    POWERFUL_WORD_LIST.append(word.strip())
f.close()

TAC_PAIRS_DIR_PATH = './tac_pairs'

# function : extract_features(row)
# extract user_id, number of propagation words, text_length, number of hashtags, number of powerful words,
# number of personal pronouns, number of retweets from given row of twitter message
# input : a twitter message in the form of (user_id, text, num_retweet, num_favorite, num_hashtag, created_time)
# output : a dictionary containing 'user_id', 'num_propagation_words', 'text_length', 'num_hashtag',
#         'num_powerful_words', 'num_personal_pronoun', 'num_retweet'
def extract_features(row):
    (user_id, text, num_retweet, num_favorite, num_hashtag, created_time) = row
    (num_propagation_words, text_length, num_personal_pronoun, num_powerful_words) = (0, len(text), 0, 0)

    for i in PROPAGATION_WORD_LIST:
        num_propagation_words += len(text.split(i)) - 1

    for i in POWERFUL_WORD_LIST:
        num_powerful_words += len(text.split(i)) - 1

    for i in PERSONAL_PRONOUN_LIST:
        num_personal_pronoun += len(text.split(i)) - 1

    # for (morpheme, type) in Okt().pos(text):
    #     if type == 'Noun' and morpheme in PERSONAL_PRONOUN_LIST:
    #         num_personal_pronoun += 1

    feature_dict = {}
    feature_dict['user_id'] = user_id
    feature_dict['num_propagation_words'] = int(num_propagation_words)
    feature_dict['text_length'] = int(text_length)
    feature_dict['num_hashtag'] = int(num_hashtag)
    feature_dict['num_powerful_words'] = int(num_powerful_words)
    feature_dict['num_personal_pronoun'] = int(num_personal_pronoun)
    feature_dict['num_retweet'] = int(num_retweet)
    return feature_dict



# function: generate_feature_data
# generates 'feature_data_save.npy', containing feature data from twitter messages.
# TAC Pairs are read from './tac_pairs/*'.
# input : none
# output : none
def generate_feature_data():
    data = []
    for file_name in os.listdir(TAC_PAIRS_DIR_PATH):
        file_path = TAC_PAIRS_DIR_PATH + '/' + file_name
        file = open(file_path, 'r', encoding='utf-8')
        csv_reader = csv.reader(file)

        is_field_row = True
        for row in csv_reader:
            if is_field_row:
                is_field_row = False
                continue
            feature_dict = extract_features(row)
            data.append(feature_dict)
        file.close()

    data_save = np.array(data)
    np.save("feature_data_save", data_save)


# function: generate_final_data
# reads feature_data_save.npy and tag results to each TAC Pair.
# generate two files 'input_data', and 'out_data'.
# 'input_data' contains # of features of a TAC Pair(data1, data2) in form of
# (data1_propagation_words, data1_text_length, data1_num_hashtag, ..., data2_propagation_words, data2_text_length, ...)
# 'output_data' contains 0, or 1. 0 meaning data1 has higher number of retweets, 1 meaning data2 has higher number of retweets.
# input: none
# output: none
def generate_final_data():
    data = np.load("feature_data_save.npy", allow_pickle=True)
    tac_user = []
    X = []
    y = []

    for row in data:
        tac_user.append(row)
        tac_len = len(tac_user)
        if tac_len > 0 and not(tac_user[tac_len-2]['user_id'] == tac_user[tac_len-1]['user_id']):
            tac_pair_list = []
            for i in range(0, tac_len):
                for j in range(i + 1, tac_len):
                    (data1, data2) = (tac_user[i], tac_user[j])
                    # only pairs those having sum of more than 10 retweets are considered meaningful
                    if (data1['num_retweet'] + data2['num_retweet'] >= 10):
                        tac_pair_list.append((data1, data2))

            for tac_pair in tac_pair_list:
                (data1, data2) = tac_pair

                input_element = []

                for i in (data1, data2):
                    input_element.append([
                        i['num_propagation_words'],
                        i['text_length'],
                        i['num_hashtag'],
                        i['num_powerful_words'],
                        i['num_personal_pronoun']
                    ])
                X.append(input_element)

                if (data1['num_retweet'] > data2['num_retweet']):
                    y.append(0)
                else:
                    y.append(1)
            tac_user = []

    X = np.array(X)
    y = np.array(y)
    print (np.shape(X))
    print (np.shape(y))
    input_data_path = "input_data";
    output_data_path = "output_data";
    np.save(input_data_path, X)
    np.save(output_data_path, y)


# extract features from TAC Pair and reshape data into the form of input and output for classifier models
generate_feature_data()
generate_final_data()
