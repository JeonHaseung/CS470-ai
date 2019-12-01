import os

f = open('./good_or_bad_words.txt', 'r')
g = open('./real_good_words.txt', 'w')
for word in f.readlines():
    word = word.split(':')
    candidate = word[0]
    word = word[1].replace('/n','').split(',')
    num_good = int(word[0])
    num_bad = int(word[1])
    total = num_good + num_bad
    if(num_good + num_bad > 1000):
        if(num_good / total > 0.66):
            g.write(candidate + '\n')
g.close()
f.close()


