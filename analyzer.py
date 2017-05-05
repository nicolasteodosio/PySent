# -*- coding: utf-8 -*-
import codecs
import os

from unidecode import unidecode

import connections
import pandas as pd

from oscar_timeline import OSCAR_TIMELINE

COLLECTION = '#Oscars'


def get_all_collection_data():
    with connections.get_db_connection() as client:
        mongo_collection = client['tweets'][COLLECTION]
        tweets = mongo_collection.find({})
        tweets_to_use = []
        for tweet in tweets:
            tweet_useful_dict = {'id': tweet['_id'],
                                 # 'sentiment': tweet['sentiment']['classification'],
                                 'eg': tweet['sentiment']['p_neg'],
                                 # 'prob_pos': tweet['sentiment']['p_pos'],
                                 'date': tweet['created_at_datetime']
                                 }
            tweets_to_use.append(tweet_useful_dict)
        tweet_frames = pd.DataFrame.from_records(tweets_to_use, columns=['eg', 'date'], index='date')
        # tweet_frames2 = pd.DataFrame.from_records(tweets_to_use, columns=['prob_neg', 'date'], index='date')
        tweet_frames = tweet_frames.groupby('eg').resample('5T').count()
        # tweet_frames2 = tweet_frames2.groupby('prob_neg').resample('5T').count()
        # oscar_frame = pd.DataFrame.from_records(OSCAR_TIMELINE, columns=['event', 'date'])

        tweet_file = codecs.open(os.path.abspath('teste/tweet.csv'), 'w', encoding='utf-8')
        # tweet_file2 = codecs.open(os.path.abspath('teste/tweet2.csv'), 'w', encoding='utf-8')

        for line in tweet_frames.to_csv(encoding='utf-8'):
            tweet_file.write(unidecode(line))
        # for line in tweet_frames2.to_csv(encoding='utf-8'):
        #     tweet_file2.write(unidecode(line))

        tweet_file.close()
        # tweet_file2.close()


def get_location_collection_data():
    with connections.get_db_connection() as client:
        mongo_collection = client['tweets'][COLLECTION]
        tweets = mongo_collection.find({})
        tweets_to_use = []
        for tweet in tweets:
            if tweet['user']['location']:
                tweet_useful_dict = {'id': tweet['_id'],
                                     'prob_pos': tweet['sentiment']['p_pos'],
                                     'eg': tweet['sentiment']['p_neg'],
                                     'location ': tweet['user']['location']
                                     }
            else:
                continue
            tweets_to_use.append(tweet_useful_dict)
        tweet_frames = pd.DataFrame.from_records(tweets_to_use)
        tweet_file = codecs.open(os.path.abspath('teste/tweet.csv'), 'w', encoding='utf-8')

        for line in tweet_frames.to_csv(encoding='utf-8'):
            tweet_file.write(unidecode(line))


def get_lang_collection_data():
    with connections.get_db_connection() as client:
        mongo_collection = client['tweets'][COLLECTION]
        tweets = mongo_collection.find({})
        tweets_to_use = []
        for tweet in tweets:
            tweet_useful_dict = {'id': tweet['_id'],
                                 'sentiment': tweet['sentiment']['classification'],
                                 'lang': tweet['lang']
                                 }
            tweets_to_use.append(tweet_useful_dict)
        tweet_frames = pd.DataFrame.from_records(tweets_to_use)
        tweet_file = codecs.open(os.path.abspath('teste/tweet.csv'), 'w', encoding='utf-8')

        for line in tweet_frames.to_csv(encoding='utf-8'):
            tweet_file.write(unidecode(line))


def get_all_collection_data_freqdist():
    with connections.get_db_connection() as client:
        mongo_collection = client['tweets'][COLLECTION]
        tweets = mongo_collection.find({})
        tweets_to_use = []
        for tweet in tweets:
            tweet_useful_dict = {'id': tweet['_id'],
                                 'sentiment': tweet['sentiment']['classification'],

                                 'date': tweet['created_at_datetime'],
                                 'text': tweet['text']
                                 }
            tweets_to_use.append(tweet_useful_dict)
        tweet_frames = pd.DataFrame.from_records(tweets_to_use, columns=['sentiment', 'date', 'text'], index='date')
        tweet_frames = tweet_frames.groupby('sentiment').resample('5T').apply(junta_tudo)
        # import ipdb; ipdb.set_trace()

        # tweet_file = codecs.open(os.path.abspath('teste/tweet.csv'), 'w', encoding='utf-8')
        #
        for line in tweet_frames:
            print line
            #     tweet_file.write(unidecode(line))
            #
            # tweet_file.close()

def junta_tudo(algo):
    teste = []
    for a in algo:
        teste.append(a)
    return teste

if __name__ == '__main__':
    get_location_collection_data()