# -*- coding: utf-8 -*-
import tweepy
from unidecode import unidecode
from conf import consumer_key, consumer_secret, access_token, access_secret


def api_access():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api


def get_tweets_timeline():
    api = api_access()

    public_tweets = api.home_timeline()

    for tweet in public_tweets:
        print "Tweet from : %s \n  tweet: %s" % (tweet.user.screen_name, tweet.text)

    print "##################################################"


def get_tweets_in_search():
    api = api_access()
    tweets = api.search(q='#primeiroassedio')

    for tweet in tweets:
        print "Tweet: {}".format(unidecode(tweet.text))
        print "##################################################"


# get_tweets_timeline()
get_tweets_in_search()


