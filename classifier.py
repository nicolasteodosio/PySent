# -*- coding: utf-8 -*-
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from pymongo import MongoClient
from os.path import join as pjoin
import unicodecsv as csv
from unidecode import unidecode


def get_db_connection():
    client = MongoClient()
    return client


def get_data():
    with get_db_connection() as client:
        tweets = client['tweets']['#TheVoiceKidsBr'].find({})
        return tweets


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
            positive_file = pjoin("word_database", "positive.csv")
            negative_file = pjoin("word_database", "negative.csv")

            with open(positive_file, 'r') as pos, open(negative_file, 'r') as neg:

                positives = list(csv.reader(pos, delimiter=',', encoding='utf-8',))
                negatives = list(csv.reader(neg, delimiter=',', encoding='utf-8',))

                posfeats = [(dict({unidecode(word[0].lower()): True}), 'pos') for word in positives]
                negfeats = [(dict({unidecode(word[0].lower()): True}), 'neg') for word in negatives]

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
