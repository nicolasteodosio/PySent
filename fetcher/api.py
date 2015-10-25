# -*- coding: utf-8 -*-
from pymongo import MongoClient
import tweepy
from conf import consumer_key, consumer_secret, access_token, access_secret
from fetcher.helper import SEARCH_QUERY


def get_api_access():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api


def get_db_connection():
    client = MongoClient()
    return client


def search(q):
    api = get_api_access()
    return api.search(q=q, lang='pt', result_type='recent', count=100)


def main():

    q = SEARCH_QUERY
    tweets = search(q)

    if tweets:
        tweets_json = []
        for tweet in tweets:
            tweets_json.append(tweet._json)

        client = get_db_connection()
        db = client['tweets']
        collection = db[q]

        result = collection.insert_many(tweets_json)
        print '{0} registros salvos!'.format(len(result.inserted_ids))


if __name__ == "__main__":
    main()


