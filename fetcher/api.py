# -*- coding: utf-8 -*-
import celery
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


@celery.task
def search(q):
    with connections.get_db_connection() as client:
        latest = get_latest_tweet(q)
        tweets = get_tweets(q, latest)

        if tweets:
            db = client['tweets']
            collection = db[q]

            result = collection.insert_many(tweets)
            print '{0} tweets saved!'.format(len(result.inserted_ids))
        else:
            print 'new tweets not found'

        return


