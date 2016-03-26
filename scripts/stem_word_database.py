# -*- coding: utf-8 -*-
import codecs
import os
from normalizer import TweetNormalizer

normalizer = TweetNormalizer('portuguese')
DATABASE_DIR = 'word_database/'


def stem_databases(database_name):
    positive_file = codecs.open(os.path.abspath(DATABASE_DIR + database_name + '/positive/pos.txt'), encoding='utf-8')
    negative_file = codecs.open(os.path.abspath(DATABASE_DIR + database_name + '/negative/neg.txt'), encoding='utf-8')

    new_positive_file = codecs.open(os.path.abspath(DATABASE_DIR + database_name + '_stem/positive/pos.txt'), 'w', encoding='utf-8')
    new_negative_file = codecs.open(os.path.abspath(DATABASE_DIR + database_name + '_stem/negative/neg.txt'), 'w', encoding='utf-8')

    for line in negative_file:
        new_negative_file.write(normalizer.stem(line) + '\n')

    for line in positive_file:
        new_positive_file.write(normalizer.stem(line) + '\n')

    positive_file.close()
    new_positive_file.close()
    negative_file.close()
    new_negative_file.close()

