# -*- coding: utf-8 -*-
import nltk
from pymongo import MongoClient


def get_db_connection():
    client = MongoClient()
    return client


def get_data():
    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    with get_db_connection() as client:
        tweets = client['tweets']['#Esquenta'].find({})
        for tweet in tweets:
            print sent_tokenizer.tokenize(tweet['text'])
            print'\n'


get_data()
