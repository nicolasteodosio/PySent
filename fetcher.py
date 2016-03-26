# -*- coding: utf-8 -*-
import tweepy

import connections
from conf import consumer_key, consumer_secret, access_token, access_secret


def get_api_access():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api


def get_tweets(q, latest=None):
    api = get_api_access()
    response = api.search(q=q, result_type='recent', count=100, since_id=latest)
    tweets = []

    for tweet in response:
        tweets.append(tweet._json)

    return tweets


def get_latest_tweet(q):
    with connections.get_db_connection() as client:
        collection = client['tweets'][q]
        try:
            return collection.find({}).sort('id', -1)[0].get('id_str')
        except IndexError:
            return None


def get_latests_tweets(q):
    latest = get_latest_tweet(q)
    return get_tweets(q, latest)
