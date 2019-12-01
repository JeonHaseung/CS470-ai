# extract influential words referring frequent_words.txt and store into good_or_bad_words.txt
import os

BASE_DIR_PATH = './timelines'
TEXT_BEGIN_DETECTOR = '"text" : "'
TEXT_END_DETECTOR = '", "truncated" : '
RETWEET_BEGIN_DETECTOR = '"retweet num" : "'
RETWEET_END_DETECTOR = '", "favorite num" : '

frequent_word_list = []
f = open('./frequent_words.txt', 'r')
for word in f.readlines():
    frequent_word_list.append(word.strip())

f.close()

done_word_list = []
f = open('./good_or_bad_words.txt', 'r')
for word in f.readlines():
    w = word.strip().split(':')[0]

    if not (w in done_word_list):
        done_word_list.append(w)

f.close()


g = open('./good_or_bad_words.txt', 'a+')

word_num = len(frequent_word_list)
word_cnt = len(done_word_list)

for word in frequent_word_list:
    if word in done_word_list:
        continue

    word_cnt += 1
    (good_users, bad_users) = (0, 0)

    print ('word({}/{})'.format(word_cnt, word_num))

    for dir in os.listdir(BASE_DIR_PATH):
        dir_path = BASE_DIR_PATH + '/' + dir
        cnt = 0
        file_num = len(os.listdir(dir_path))

        for file in os.listdir(dir_path):
            cnt += 1
            file_path = dir_path + '/' + file

            f = open(file_path, 'r')

            (sum_yes, sum_no) = (0, 0)
            (count_yes, count_no) = (0, 0)

            for line in f.readlines():
                text_begin_position = line.find(TEXT_BEGIN_DETECTOR) + len(TEXT_BEGIN_DETECTOR)
                text_end_position = line.find(TEXT_END_DETECTOR)
                retweet_begin_position = line.find(RETWEET_BEGIN_DETECTOR) + len(RETWEET_BEGIN_DETECTOR)
                retweet_end_position = line.find(RETWEET_END_DETECTOR)

                if (text_begin_position < 0 or text_end_position < 0 or retweet_begin_position < 0 or retweet_end_position < 0):
                    continue

                text = line[text_begin_position : text_end_position]
                retweet_num = int(line[retweet_begin_position : retweet_end_position])

                if word in line:
                    sum_yes += retweet_num
                    count_yes += 1
                else:
                    sum_no += retweet_num
                    count_no += 1

            if count_yes == 0 or count_no == 0:
                continue

            if sum_yes / (count_yes + 0.0) > sum_no / (count_no + 0.0):
                good_users += 1
            else:
                bad_users += 1

            f.close()

    #print ('{}:{},{}'.format(word, good_users, bad_users))
    g.write('{}:{},{}'.format(word, good_users, bad_users))
    g.write('\n')

g.close()
