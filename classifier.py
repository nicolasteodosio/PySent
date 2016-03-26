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

        self.stopSet = set(stopwords.words('english'))

    def get_data(self, hashtag):
        with connections.get_db_connection() as client:
            tweets = client['tweets'][hashtag].find({'retweeted': False})
            return tweets

    def classify_some(self, hashtag):
        for tweet in self.get_data(hashtag)[:100]:
            blob = TextBlob(tweet['text'], analyzer=CustomNaiveBayesAnalyzer())
            print 'Tweet: {} || analisys: {}'.format(unidecode(tweet['text']), blob.sentiment)

    def classify(self, text, analyzer):
        blob = TextBlob(text, analyzer=analyzer)

        return blob.sentiment


class CustomNaiveBayesAnalyzer(NaiveBayesAnalyzer):
    def _default_feature_extractor(words):
        """Default feature extractor for the NaiveBayesAnalyzer."""
        return dict(((word, True) for word in words))

    def __init__(self, feature_extractor=_default_feature_extractor, databases=['senti_lex']):
        super(NaiveBayesAnalyzer, self).__init__()
        self._classifier = None
        self.feature_extractor = feature_extractor
        self.databases = databases

    def train(self):
        """Train the Naive Bayes classifier on the movie review corpus."""
        super(NaiveBayesAnalyzer, self).train()

        neg_feats = []
        pos_feats = []

        for database in self.databases:
            neg_txt_file = open(os.path.abspath('word_database/' + database + '/negative/neg.txt'))
            pos_txt_file = open(os.path.abspath('word_database/' + database + '/positive/pos.txt'))

            neg_feats.append((self.feature_extractor([line.rstrip('\n') for line in neg_txt_file]), 'neg'))
            pos_feats.append((self.feature_extractor([line.rstrip('\n') for line in pos_txt_file]), 'pos'))

        train_data = neg_feats + pos_feats

        self._classifier = nltk.classify.NaiveBayesClassifier.train(train_data)