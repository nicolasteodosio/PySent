# -*- coding: utf-8 -*-
import nltk
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


class CustomNaiveBayesAnalyzer(NaiveBayesAnalyzer):
    def _default_feature_extractor(words):
        """Default feature extractor for the NaiveBayesAnalyzer."""
        return dict(((word, True) for word in words))

    def __init__(self, feature_extractor=_default_feature_extractor, corpus=None):
        super(NaiveBayesAnalyzer, self).__init__()
        self._classifier = None
        self.feature_extractor = feature_extractor

    def train(self):
        """Train the Naive Bayes classifier on the movie review corpus."""
        super(NaiveBayesAnalyzer, self).train()
        import ipdb; ipdb.set_trace()
        neg_ids = nltk.corpus.movie_reviews.fileids('neg')
        pos_ids = nltk.corpus.movie_reviews.fileids('pos')
        neg_feats = [(self.feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
        pos_feats = [(self.feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]
        train_data = neg_feats + pos_feats
        self._classifier = nltk.classify.NaiveBayesClassifier.train(train_data)