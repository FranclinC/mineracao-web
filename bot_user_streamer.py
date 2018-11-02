# from tweepy.streaming import StreamListener
import pandas as pd
import numpy as np
import glob
import os
import csv
import tweepy

import twitter_credentials

class UserLogInApi():
    
    def __init__(self):
        pass
    
    def authenticate(self):
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        
        api = tweepy.API(auth)
        
        print ("Returning api")
        return api
        

"""
class UserStreamListener(StreamListener):
    
    def __init__ (self, user_ids):


    def on_status(self, status):
        return False

    def on_error(self, status):
        self.csv_file.close()
        return False
"""

def get_all_tweets(user_id):
    try:
        alltweets = []
        
        new_tweets = api.user_timeline(user_id = user_id, count = 200)
    
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        
        while len(new_tweets) > 0:
            print ("getting tweets before %s" % (oldest))
            
            new_tweets = api.user_timeline(user_id = user_id, count = 200, max_id = oldest)
            
            alltweets.extend(new_tweets)
            
            oldest = alltweets[-1].id - 1
            
            print ("...%s tweets downloaded so far" % (len(alltweets)))
            
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
        
        with open('user_tweets/%s_tweets.csv' % user_id, 'w', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            writer.writerows(outtweets)
    except tweepy.TweepError:
        print ("Can't get access to this user, skipping it.")
        
    pass
    

if __name__ == "__main__":

    path = "hashtags/"
    files = glob.glob(os.path.join(path, "*.csv"))
    data_from_files = (pd.read_csv(file) for file in files)

    concatenated_files = pd.concat(data_from_files, ignore_index = True)

    users_ids = concatenated_files[["user_id"]]
    
    userStreamer = UserLogInApi()
    api = userStreamer.authenticate()

    amount_users = len(users_ids)
    
    for i in range(amount_users):
        user_id = users_ids.iloc[i, :].values
        print ("Getting user with id: %s" % (user_id))
        get_all_tweets(user_id[0])
    
    #user_id = users_ids.iloc[1, :].values
    
    #get_all_tweets(user_id[0])
    

    
    
    

    