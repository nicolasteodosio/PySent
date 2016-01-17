# coding: utf-8


# Remove hashtags, mentions, links
def clean_tweets(tweets):
    clean_data = []
    for tweet in tweets:
        item = ' '.join(word.lower() for word in tweet.split() \
                        if not word.startswith('#') and \
                        not word.startswith('@') and \
                        not word.startswith('http') and \
                        not word.startswith('RT'))
        if item == "" or item == "RT":
            continue
        clean_data.append(item)
    return clean_data
