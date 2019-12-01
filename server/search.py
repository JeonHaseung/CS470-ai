# -*- coding:utf-8 -*-
# using twitter api(tweepy), crawl raw json data and make data_search.txt.
import tweepy
from constants import *


def list_to_query(list):
    return ' OR '.join(list)


auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# tweepy의 limit이 있어 기다리게 해주기
api = tweepy.API(auth, wait_on_rate_limit=True)

query = list_to_query(URL_DETECTOR_WORD_LIST)

# count는 100이 최대
# tweet_mode='extended'로 지정하면 140자 넘어도 안잘리지만, .text 인자가 .full_text 인자로 대체됨
pages = tweepy.Cursor(
    api.search,
    q=query,
    count=100,
    tweet_mode='extended',
    lang='ko',
    show_user=True
).pages()

for page in pages:
    for post in page:
        print(post._json)
