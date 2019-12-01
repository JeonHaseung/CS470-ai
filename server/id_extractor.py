import os
import json
import tweepy
from constants import *

f = open('data_search1.txt', 'r')
# f = open('data_streaming.txt', 'r')
contentlist = f.readlines()

id_list = []
print('Getting Content List')
print('##########################################')
for i in range(len(contentlist)):
    index_id = contentlist[i].index('id')
    index_id_end = contentlist[i].index('id_str')
    index_text = contentlist[i].index('text')
    index_text_end = contentlist[i].index('truncated')
    content_id = contentlist[i][index_id + 5:index_id_end - 3]
    content_text = contentlist[i][index_text + 12:index_text_end - 3]
    if(content_id in id_list):
        print('1')
    else:
        id_list.append(content_id)
    print('Content : ' + str(i / len(contentlist)) + '% Done (' + str(i) + ' / ' + str(len(contentlist)) + ')')
# print(id_list)

print('##########################################')
auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

# print('1126032219745599488' in id_list)
# userid = json.loads(json.dumps(api.get_status(id_list[i])._json))['user']['id']
# print(len(api.user_timeline(userid)))

print('Getting ID List')
print('##########################################')
for i in range(len(id_list)):
    try: 
        userid = json.loads(json.dumps(api.get_status(id_list[i])._json))['user']['id']
        f = open('./timelines/wtf1/' + str(userid) + '.txt', 'w')
        followernum = int(json.loads(json.dumps(api.get_status(id_list[i])._json))['user']['followers_count'])
        if followernum > 100:
            timeline = api.user_timeline(userid, tweet_mode='extended')
            for j in range(len(timeline)):
                jsony = timeline[j]._json
                hashlist = jsony['entities']['hashtags']
                urllist = jsony['entities']['urls']
                if(len(urllist) > 0):
                    f.write('{')
                    f.write('\"user id\" : \"' + str(jsony['user']['id']) + '\", ')
                    f.write('\"user name\" : \"' + str(jsony['user']['name']) + '\", ')
                    f.write('\"user screen_name\" : \"' + str(jsony['user']['screen_name']) + '\", ')
                    if('media' in jsony['entities']):
                        f.write('\"media\" : \"' + str(jsony['entities']['media']) + '\", ')
                    f.write('\"post id\" : \"' + str(jsony['id']) + '\", ')
                    f.write('\"created at\" : \"' + str(jsony['created_at']) + '\", ')
                    f.write('\"text\" : \"' + str(jsony['full_text']).replace('\"','\'').replace('\n','') + '\", ')
                    f.write('\"truncated\" : \"' + str(jsony['truncated']) + '\", ')
                    f.write('\"hashtag num\" : \"' + str(len(hashlist)) + '\", ')
                    f.write('\"retweet num\" : \"' + str(jsony['retweet_count']) + '\", ')
                    f.write('\"favorite num\" : \"' + str(jsony['favorite_count']) + '\", ')
                    f.write('\"lang\" : \"' + str(jsony['lang']) + '\", ')
                    f.write('\"url\" : \"[')
                    for k in range(len(urllist)):
                        f.write(str(urllist[k]['url']))
                        if(k < len(urllist) - 1):
                            # print(k, len(urllist))
                            f.write(', ')
                    f.write(']\"')
                    f.write('}\n')
    except tweepy.TweepError:   
        print('Ang gimmotti') 
    print('ID : ' + str(i / len(id_list)) + '% Done (' + str(i) + ' / ' + str(len(id_list)) + ')')
print('##########################################')

