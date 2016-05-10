# -*- coding: utf-8 -*-
import connections


def create_tweets_base(q='#OscarNaSKY'):
    with connections.get_db_connection() as client:
        collection = client['tweets'][q]
        tweets = collection.find({})
        for tweet in tweets:
            print tweet.get('text')
            polarity = input('Positivo:1, Negativo:0, Irrelevante:3 \n')
            if polarity == 1:
                client['tweets']['pos'].insert(tweet)
            elif polarity == 0:
                client['tweets']['neg'].insert(tweet)
            else:
                continue
