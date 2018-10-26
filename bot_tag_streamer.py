
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import csv
import argparse

class TwitterStreamer():

    def __init__(self):
        pass
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, max_tweets):
        listener = TwitterListener(fetched_tweets_filename, max_tweets)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list, languages=["pt"], async=True)

class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename, max_tweets):
        super().__init__()
        self.fetched_tweets_filename = fetched_tweets_filename
        self.csv_file = open(self.fetched_tweets_filename, 'a')
        self.csv_writer = csv.writer(self.csv_file)
        self.max_tweets = max_tweets

        self.csv_writer.writerow([
            "id",
            "text",
            "user_id",
            "num_hashtags",
            "num_urls",
            "num_mentions",
            "retweet_count",
            "favorite_count",
            "place",
            "timestamp"
        ])

    def on_status(self, status):
        id = status.id
        text = status.text
        user_id = status.user.id
        num_hashtags = len(status.entities["hashtags"])
        num_urls = len(status.entities["urls"])
        num_mentions = len(status.entities["user_mentions"])
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        timestamp = status.timestamp_ms
        place = status.place
        
        if place is None:
            final_place = place
        else:
            final_place = place.full_name

        self.csv_writer.writerow([
            id,
            text,
            user_id,
            num_hashtags,
            num_urls,
            num_mentions,
            retweet_count,
            favorite_count,
            final_place,
            timestamp
        ])
        self.max_tweets -= 1

        if self.max_tweets < 0:
            return False
        
        return True

    def on_error(self, status):
        if status == 420:
            self.csv_file.close()
            return False        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group("required arguments")
    required.add_argument("-m", "--max-tweets", dest="max_tweets", help="Number of tweets to be retrieved", required=True)
    required.add_argument("-t", "--terms", dest="hash_tag_list", help="List of terms", nargs="+", required=True)
    required.add_argument("-o", "--output", dest="fetched_tweets_filename", help="Output file", required=True)
    
    args = parser.parse_args()

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(args.fetched_tweets_filename, args.hash_tag_list, int(args.max_tweets))