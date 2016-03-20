# -*- coding: utf-8 -*-
import celery
from datetime import datetime
from unidecode import unidecode
from classifier import CustomNaiveBayesAnalyzer, SentimentClassifier
import connections
from fetcher import get_latest_tweet, get_tweets

DATABASES = ['senti_lex', 'puc_portuguese', 're_li']

classifier = SentimentClassifier()
analyzer = CustomNaiveBayesAnalyzer(databases=DATABASES)


@celery.task
def search(q):
    with connections.get_db_connection() as client:
        latest = get_latest_tweet(q)
        tweets = get_tweets(q, latest)

        if not tweets:
            print 'There are NO new tweets'
        else:
            print '{0} new tweets fetched!'.format(len(tweets))

            for tweet in tweets:
                sentiment = classifier.classify(tweet['text'], analyzer)

                # Creating the 'neutral' classification to measure the accuracy of the model
                if sentiment.p_pos == .5:
                    classification = 'neu'
                else:
                    classification = sentiment.classification

                tweet['sentiment'] = {
                    'classification': classification,
                    'p_pos': sentiment.p_pos,
                    'p_neg': sentiment.p_neg,
                    'databases': DATABASES,
                    'classificated_at': datetime.now()
                }

            db = client['tweets']
            collection = db[q]

            result = collection.insert_many(tweets)
            print '{0} tweets classified'.format(len(result.inserted_ids))

        return