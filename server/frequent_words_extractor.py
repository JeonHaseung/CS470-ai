# extract words written more than 10 times and save in frequent_words.txt
import os
import re

BASE_DIR_PATH = './timelines'
FILTER_STR_LIST = "/\/n~!@#$%^&*()_+`1234567890-=[]{};:',./<>?\|）abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZα.:·'-—'',"
TEXT_BEGIN_DETECTOR = '"text" : "'
TEXT_END_DETECTOR = '", "truncated" : '

word_dictionary = {}

for dir in os.listdir(BASE_DIR_PATH):
    # if not (dir == 'wtf16' or dir == 'wtf18'):
    #     continue

    dir_path = BASE_DIR_PATH + '/' + dir
    cnt = 0
    file_num = len(os.listdir(dir_path))
    for file in os.listdir(dir_path):
        cnt += 1

        print ('{}, ({}/{})'.format(dir_path + '/' + file, cnt, file_num))
        file_path = dir_path + '/' + file

        f = open(file_path, 'r')

        for line in f.readlines():
            text_begin_position = line.find(TEXT_BEGIN_DETECTOR) + len(TEXT_BEGIN_DETECTOR)
            text_end_position = line.find(TEXT_END_DETECTOR)
            text = line[text_begin_position : text_end_position]

            for filter_str in FILTER_STR_LIST:
                if filter_str in text:
                    text = text.replace(filter_str, '')

            text = re.sub('\s+', ' ', text.strip())

            for word in text.split():
                if word_dictionary.get(word):
                    word_dictionary[word] += 1
                else:
                    word_dictionary[word] = 1
        f.close()

f = open('frequent_words.txt', 'w')
for word in word_dictionary.keys():
    if word_dictionary[word] >= 10:
        f.write(word)
        f.write('\n')

f.close()
