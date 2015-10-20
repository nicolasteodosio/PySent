# -*- coding: utf-8 -*-
import tweepy
from conf import consumer_key, consumer_secret, access_token, access_secret


def get_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()

    for tweet in public_tweets:
        print "Tweet from : %s \n  tweet: %s" % (tweet.user.screen_name, tweet.text)

    print "##################################################"

    test = api.trends_available()

    print test[0]

get_tweets()


