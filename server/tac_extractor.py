import os
import json
import tweepy
from constants import *

# check entities url and extract TAC Pairs from [id].txt
tacpair = [] 
for q in range(1):
    qq = q + 1
    g = open('./tac_pair/tac_pair' + str(qq) + '.csv', 'w')
    csvs = 'user id, text, retweet, favorite, hashtag, create time'
    g.write(csvs + '\n')
    csvs = ''
    filelength = len(os.listdir('./timelines/wtf' + str(qq)))
    cnt = 0
    for filename in os.listdir('./timelines/wtf' + str(qq)):
        f = open('./timelines/wtf' + str(qq) + '/' + filename, 'r')
        statuses = f.readlines()
        urllist = {}
        idlist = {}
        textlist = {}
        retweetlist = {}
        favoritelist = {}
        hashtaglist = {}
        createlist = {}
        cnt += 1
        print('TAC Extractor : ' + str(cnt / filelength) + '(' + str(cnt) + ' / ' + str(filelength) + ')')
        try: 
            for i in range(len(statuses) - 1):
                statuses[i] = json.loads(statuses[i])
                urls = statuses[i]['url'].split(',')
                for k in range(len(urls)):
                    if(urls[k] not in urllist):
                        urllist[urls[k]] = []
                        idlist[urls[k]] = []
                        textlist[urls[k]] = []
                        retweetlist[urls[k]] = []
                        favoritelist[urls[k]] = []
                        hashtaglist[urls[k]] = []
                        createlist[urls[k]] = []
                    urllist[urls[k]].append(statuses[i]['post id'])
                    idlist[urls[k]].append(statuses[i]['user id'])
                    textlist[urls[k]].append(statuses[i]['text'])
                    retweetlist[urls[k]].append(statuses[i]['retweet num'])
                    favoritelist[urls[k]].append(statuses[i]['favorite num'])
                    hashtaglist[urls[k]].append(statuses[i]['hashtag num'])
                    createlist[urls[k]].append(statuses[i]['created at'])
            for i in urllist.keys():
                if(len(urllist[i]) > 1):
                    tacpair.append(urllist[i])
                    for j in range(len(urllist[i])):
                        csvs = csvs + str(idlist[i][j]) + ','
                        csvs = csvs + str(textlist[i][j].replace(',', '')) + ','
                        csvs = csvs + str(retweetlist[i][j]) + ','
                        csvs = csvs + str(favoritelist[i][j]) + ','
                        csvs = csvs + str(hashtaglist[i][j]) + ','
                        csvs = csvs + str(createlist[i][j])
                        g.write(csvs + '\n')
                        csvs = ''
        except ValueError as e:
            print(e)
    f = open('tacpairlist' + str(qq) + '.txt', 'w')
    f.write(str(tacpair))
