# -*- coding: utf-8 -*-
import celery
import connections
from fetcher import get_latest_tweet, get_tweets


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


