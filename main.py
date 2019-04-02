import os
import json
import datetime
from TwitterAPI import TwitterAPI
from dateutil.parser import parse
from dateutil.tz import gettz

import config

tzinfos = {"CST": gettz("Asia/Jerusalem")}


SEARCH_TERM = "גנץ"
NUMBER_OF_TWEETS = 10
now = datetime.datetime.now()
outputDirectory = os.path.join(os.getcwd(), "output")

fileName = "%s_%d%02d%02d-%02d%02d%02d" % (SEARCH_TERM, now.year, now.month, now.day, now.hour, now.minute, now.second)
if __name__ == '__main__':
    api = TwitterAPI(config.API_KEY, config.API_SECRET, auth_type='oAuth2')
    r = api.request('search/tweets', {'q': SEARCH_TERM, 'lang': 'he', 'count': 100})

    # for item in r:
    #     print(item['text'] if 'text' in item else item)
    tweets = r.response.json()
    firstTweetCreatedAt = tweets['statuses'][0]['created_at']
    print("first tweet created at: %s" % firstTweetCreatedAt)
    print(parse(firstTweetCreatedAt, tzinfos=tzinfos))
    with open(os.path.join(outputDirectory, "csv", "%s.csv" % fileName), "w") as outputCsv:
        headers = "tweet_id\tcreated_at\tuser_name\tuser_handle\ttext\tmentions_handles\turls\thashtags\tfavorite_count\tretweet_count"
        outputCsv.write(headers+"\n")
        for tweet in tweets['statuses']:
            createdAt = parse(tweet['created_at'], tzinfos=tzinfos)
            mentions_usernames = []
            for user_mention in tweet['entities']['user_mentions']:
                mentions_usernames.append(user_mention['screen_name'].encode('utf-16'))
            tweet_urls = []
            for url in tweet['entities']['urls']:
                tweet_urls.append(url['url'])
            tweet_hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                tweet_hashtags.append(hashtag['text'].encode('utf-16'))
            line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%d\n" % (tweet['id_str'], createdAt, tweet['user']['name'].encode('utf-16'),
                                                                 tweet['user']['screen_name'].encode('utf-16'), tweet['text'].encode('utf-16'), mentions_usernames,
                                                                 tweet_urls, tweet_hashtags, tweet['retweet_count'], tweet['favorite_count'])

            outputCsv.write(line)
    with open(os.path.join(outputDirectory, "json", "%s.json" % fileName), "w") as fileWriter:
        fileWriter.write(json.dumps(r.response.json()))
    print("Output written to file")

    exit(1)
