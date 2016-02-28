# -*- coding: utf-8 -*-
from nltk.corpus import stopwords

from unidecode import unidecode
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import connections
import os


class SentimentClassifier(object):
    def __init__(self):
        """
        Constructs a new SentimentAnalyzer instance.
        """

        collection = os.environ.get('HASHTAG')
        self.data = self.get_tweets_data(collection)
        self.stopSet = set(stopwords.words('english'))

    def get_tweets_data(self, hashtag):
        with connections.get_db_connection() as client:
            tweets = client['tweets'][hashtag].find({'lang': 'en', 'retweeted': False})
            return tweets

    def classify(self):
        for tweet in self.data[:12]:
            blob = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
            print 'Tweet: {} || analisys: {}'.format(unidecode(tweet['text']), blob.sentiment)
