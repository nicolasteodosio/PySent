# -*- coding: utf-8 -*-
import tweepy
from unidecode import unidecode
from conf import consumer_key, consumer_secret, access_token, access_secret


def get_api_access():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api


def get_tweets_timeline():
    api = get_api_access()

    public_tweets = api.home_timeline()

    for tweet in public_tweets:
        print "Tweet from : %s \n  tweet: %s" % (tweet.user.screen_name, tweet.text)

    print "##################################################"


def search(q):
    api = get_api_access()
    tweets = api.search(q=q, lang='pt', result_type='recent', count=100)

    for tweet in tweets:
        print "Tweet: {}".format(unidecode(tweet.text))
        print "##################################################"


def main():
    search('#primeiroassedio')


if __name__ == "__main__":
    main()


