# -*- coding: utf-8 -*-
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from unidecode import unidecode

TWITTER_STOPWORDS = [
    '@',
    'RT',
    'http'
]


class TweetNormalizer(object):
    def __init__(self, language):
        self.language = language
        self.stemmer = SnowballStemmer(language, ignore_stopwords=True)

    def clean_stopwords(self, text):
        # Cleaning portuguese stopwords
        splitted = [i for i in text.split() if i not in stopwords.words(self.language)]
        cleaned_splitted = []

        # Cleaning twitter stopwords
        for word in splitted:
            cleaned_splitted.append(word)

            for twitter_stopword in TWITTER_STOPWORDS:
                if word.startswith(twitter_stopword):
                    cleaned_splitted.remove(word)

        return ' '.join(cleaned_splitted)

    def stem(self, text):
        splitted = text.split()

        for i, word in enumerate(splitted):
            stem_word = self.stemmer.stem(unidecode(word))
            splitted[i] = stem_word

        return ' '.join(splitted)

    def normalize(self, text):
        text = self.clean_stopwords(text)
        text = self.stem(text)

        return text
