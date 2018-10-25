
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

class TwitterStreamer():

    def __init__(self):
        pass
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=fetched_tweets_filename, async=True)

class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False        


if __name__ == "__main__":
    hash_tag_list = ["Fernando Haddad", "haddad", "Jair Bolsonaro", "PT", "PSL", "ele nao", "elenao", "eleicao2018"]
    fetched_tweets_filename = "tweets2.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)