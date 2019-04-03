import sys
import os
import json
from pathlib import Path
import datetime
import csv
from TwitterAPI import TwitterAPI
from dateutil.parser import parse
from dateutil.tz import gettz

import config

tzinfos = {"CST": gettz("Asia/Jerusalem")}

NUMBER_OF_TWEETS = 100
outputDirectory = Path(os.getcwd(), "output")


def getfilename(search_term):
    now = datetime.datetime.now()
    return "%s_%d%02d%02d-%02d%02d%02d" % (search_term, now.year, now.month, now.day, now.hour, now.minute, now.second)


def runquery(api, term, tweetMaxId):
    options = {
        'q': term,
        'lang': 'he',
        'count': NUMBER_OF_TWEETS,
        'result_type': 'recent'
    }
    if tweetMaxId > 0:
        options['max_id'] = tweetMaxId - 1
    r = api.request('search/tweets', options)
    return r.response.json()


def escapetext(text):
    return text.replace("\t", " ").replace("\n", "  <*newline*>  ")


def savetweetstocsv(tweets, targetFileName):
    headers = ["tweet_id", "created_at", "user_name", "user_handle", "text", "mentions_handles", "urls", "hashtags",
               "favorite_count", "retweet_count"]
    full_file_path = outputDirectory / "csv" / targetFileName
    csv_exists = os.path.exists(full_file_path)
    with open(full_file_path, "a", newline='', encoding='utf-8') as outputCsv:
        writer = csv.writer(outputCsv, delimiter="\t")
        if not csv_exists:
            writer.writerow(headers)
        # outputCsv.write("\n")
        for tweet in tweets['statuses']:
            createdAt = parse(tweet['created_at'], tzinfos=tzinfos)
            mentions_usernames = [x['screen_name'] for x in tweet['entities']['user_mentions']]
            tweet_urls = [x['url'] for x in tweet['entities']['urls']]
            tweet_hashtags = [x['text'] for x in tweet['entities']['hashtags']]
            line_elements = [tweet['id_str'], createdAt, tweet['user']['name'],
                             tweet['user']['screen_name'], escapetext(tweet['text']), mentions_usernames,
                             tweet_urls, tweet_hashtags, tweet['retweet_count'], tweet['favorite_count']]
            writer.writerow(line_elements)


def get_tweets_texts(tweets, existing_text):
    if existing_text is None:
        existing_text = ""
    for tweet in tweets:
        existing_text = "%s %s" % (existing_text, tweet['text'])
    return existing_text


def get_word_count(tweets_texts):
    tweets_texts = tweets_texts.split()
    d = {}
    for key in tweets_texts:
        d[key] = d.get(key, 0) + 1
    return sorted(d.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    search_term = str(input("Please type in the term you would like to search"))
    api = TwitterAPI(config.API_KEY, config.API_SECRET, auth_type='oAuth2')
    fileName = getfilename(search_term)
    numOfTweetsCollected = 0
    tweetsArray = []
    tweetMaxId = 0
    collect_counter = 0
    all_tweets_text = ""
    while numOfTweetsCollected < 500 and collect_counter < 10:
        collect_counter += 1
        tweets = runquery(api, search_term, tweetMaxId)
        all_tweets_text = "%s %s" % (all_tweets_text, get_tweets_texts(tweets['statuses'], all_tweets_text))
        if len(tweets['statuses']) == 0:
            break
        tweetsArray.append(tweets)
        tweetMaxId = tweets['statuses'][len(tweets['statuses'])-1]['id']
        numOfTweetsCollected += len(tweets['statuses'])
        jsonFileName = "%s_%d.json" % (fileName, collect_counter)
        open(outputDirectory / "json" / jsonFileName, "w").write(json.dumps(tweets))
    for tweetSet in tweetsArray:
        savetweetstocsv(tweetSet,  "%s.csv" % fileName)
    word_count = get_word_count(all_tweets_text)
    word_count_filename = outputDirectory / "csv" / ("%s_word_count.csv" % fileName)
    with open(word_count_filename, "w", newline='', encoding='utf-8') as outputCsv:
        writer = csv.writer(outputCsv, delimiter="\t")
        for item in word_count:
            writer.writerow(item)
    open("tweets_text.txt", "w").write(all_tweets_text)
    print("Output written to files output/json/%s.json and output/csv/%s.csv" % (fileName, fileName))

    exit(1)
