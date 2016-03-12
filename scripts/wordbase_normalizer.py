# -*- coding: utf-8 -*-
"""
Script para fazer a base de palavras do SentiLex
no padrão necessáio pelo textblob
"""


import os


def wordbase_normalizer():
    txt_file = open(os.path.abspath('word_database/SentiLex-PT02/SentiLex-lem-PT02.txt'), 'r')
    new_pos_file = open(os.path.abspath('word_database/SentiLex-PT02/normalized/positive/pos.txt'), 'w')
    new_neg_file = open(os.path.abspath('word_database/SentiLex-PT02/normalized/negative/neg.txt'), 'w')
    new_neut_file = open(os.path.abspath('word_database/SentiLex-PT02/normalized/neutral/net.txt'), 'w')
    for line in txt_file:
        line_split = line.split(';')
        polarity = line_split[2].split('=')[1]
        word = line_split[0].split('.')[0]
        if polarity == '1':
            new_pos_file.write(word + '.\n')
        elif polarity == '-1':
            new_neg_file.write(word + '.\n')
        else:
            new_neut_file.write(word + '.\n')
