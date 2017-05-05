# -*- coding: utf-8 -*-
import os

from classifier import SentimentClassifier, CustomNaiveBayesAnalyzer
from normalizer import TweetNormalizer

DATABASES = ['re_li']

classifier = SentimentClassifier()
analyzer = CustomNaiveBayesAnalyzer(databases=DATABASES)
normalizer = TweetNormalizer('portuguese')


def acuracy():
    txt_file = open(os.path.abspath('word_database/acuracia.txt'), 'r')
    qtd = 0
    for tweet in txt_file:
        qtd += add_classification_information(tweet)
    print qtd


def add_classification_information(tweet):
    qtd_pos=0
    normalized_text = normalizer.normalize(tweet)
    sentiment = classifier.classify(normalized_text, analyzer)
    # Creating the 'neutral' classification to measure the accuracy of the model
    if sentiment.p_pos == .5:
        classification = 'neu'
    else:
        classification = sentiment.classification

    if classification == 'pos':
        qtd_pos += 1

    return qtd_pos
