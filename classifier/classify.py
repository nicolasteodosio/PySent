# -*- coding: utf-8 -*-
import sys
import csv

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from pymongo import MongoClient
from os.path import join as pjoin


def get_db_connection():
    client = MongoClient()
    return client


def get_data():
    with get_db_connection() as client:
        tweets = client['tweets']['#Esquenta'].find({})


class SentimentAnalyzer(object):
    def __init__(self):
        """
        Constructs a new SentimentAnalyzer instance.
        """

        self.min_word_length = 3

        self.stopSet = set(stopwords.words('portuguese'))

        # Naive Bayes initialization
        self._init_naive_bayes()

    def _init_naive_bayes(self):
        """
        _init_naive_bayes(self):
        Gets the data from the positive, negative and neutral text files.
        Creates and trains the Naive Bayes classifier, using the data, so
        that it can learn what constitutes a positive, negative or neutral tweet.
        """

        try:
            positive_file = pjoin(sys.path[0], "word_database", "positive.csv")
            negative_file = pjoin(sys.path[0], "word_database", "negative.csv")

            positives = list(csv.reader(positive_file, delimiter=','))
            negatives = list(csv.reader(negative_file, delimiter=','))

            posfeats = [(dict({word.lower(): True}), 'pos') for word in positives if self._is_valid_word(word)]
            negfeats = [(dict({word.lower(): True}), 'neg') for word in negatives if self._is_valid_word(word)]

            self.classifier = NaiveBayesClassifier.train(posfeats + negfeats)

        except:
            raise Exception("Unknown error in SentimentAnalyzer::__init_naive_bayes")

    def _is_valid_word(self, word):
        """
		__check_word( self, word ):
		Input: word. The word to check.
		Looks at a word and determines whether that should be used in the classifier.
		Return: True if the word should be used, False if not.
		"""
        if word in self.stopSet \
                or len(word) < self.min_word_length \
                or word[0] == "@" \
                or word[0] == "#" \
                or word[:4] == "http":
            return False
        else:
            return True