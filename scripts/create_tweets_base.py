# -*- coding: utf-8 -*-
import os
import connections


def create_tweets_base():
    with connections.get_db_connection() as client:
        collection = client['tweets'][os.environ.get('COLLECTION')]
        tweets = collection.find({})
        for tweet in tweets:
            print tweet.get('text')
            polarity = input('Positivo:1, Negativo:0, Irrelevante:3 \n')
            if polarity == 1:
                client['tweets']['pos'].insert_one(tweet)
            elif polarity == 0:
                client['tweets']['neg'].insert_one(tweet)
            else:
                continue
