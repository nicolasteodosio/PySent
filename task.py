# -*- coding: utf-8 -*-
import time
from datetime import datetime

import celery

from classifier import CustomNaiveBayesAnalyzer, SentimentClassifier
import connections
from fetcher import get_latests_tweets
from normalizer import TweetNormalizer

# DATABASES = ['senti_lex', 'puc_portuguese', 're_li']
DATABASES = ['senti_lex_stem', 'puc_portuguese_stem', 're_li_stem', 'oscars_stem']

COLLECTIONS = ['#Oscars2016']

classifier = SentimentClassifier()
analyzer = CustomNaiveBayesAnalyzer(databases=DATABASES)
normalizer = TweetNormalizer('portuguese')


@celery.task
def search(q):
    with connections.get_db_connection() as client:
        tweets = get_latests_tweets(q)

        if not tweets:
            print 'There are NO new tweets'
        else:
            print '{0} new tweets fetched!'.format(len(tweets))

            for tweet in tweets:
                add_classification_information(tweet)

            db = client['tweets']
            collection = db[q]

            result = collection.insert_many(tweets)
            print '{0} tweets classified'.format(len(result.inserted_ids))

        return


def add_classification_information(tweet):
    normalized_text = normalizer.normalize(tweet['text'])
    sentiment = classifier.classify(normalized_text, analyzer)
    # Creating the 'neutral' classification to measure the accuracy of the model
    if sentiment.p_pos == .5:
        classification = 'neu'
    else:
        classification = sentiment.classification

    tweet['sentiment'] = {
        'normalized_text': normalized_text,
        'classification': classification,
        'p_pos': sentiment.p_pos,
        'p_neg': sentiment.p_neg,
        'databases': DATABASES,
        'classificated_at': datetime.now()
    }

    return tweet


def reclassify():
    start_time = time.time()
    for collection in COLLECTIONS:

        with connections.get_db_connection() as client:
            mongo_collection = client['tweets'][collection]
            tweets = mongo_collection.find({})

            for tweet in tweets:
                tweet_classified = add_classification_information(tweet)
                mongo_collection.replace_one({'_id': tweet['_id']}, tweet_classified)
    elapsed_time = time.time() - start_time

    print 'Time elapsed: {} seconds'.format(elapsed_time)
    return
