# -*- coding: utf-8 -*-
from nltk.corpus import stopwords

from unidecode import unidecode
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import connections
import os


class SentimentAnalyzer(object):
    def __init__(self):
        """
        Constructs a new SentimentAnalyzer instance.
        """

        collection = os.environ.get('HASHTAG')
        self.data = self.get_tweets_data(collection)
        self.stopSet = set(stopwords.words('english'))

        # Naive Bayes initialization
        self._init_naive_bayes()

    def get_tweets_data(self, hashtag):
        with connections.get_db_connection() as client:
            tweets = client['tweets'][hashtag].find({'lang': 'en', 'retweeted': False})
            return tweets

    def _init_naive_bayes(self):
        """
        _init_naive_bayes(self):
        Gets the data from the positive, negative and neutral text files.
        Creates and trains the Naive Bayes classifier, using the data, so
        that it can learn what constitutes a positive, negative or neutral tweet.
        """

        pass

    def classify(self):
        for tweet in self.data[:12]:
            blob = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
            print 'Tweet: {} || analisys: {}'.format(unidecode(tweet['text']), blob.sentiment)
