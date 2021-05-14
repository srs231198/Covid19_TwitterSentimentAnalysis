import tweepy
import socket
import re
from datetime import datetime
from elasticsearch import Elasticsearch


#Enter your Twitter keys here!!!
API_KEY = ""

API_Secret_Key = ""

Bearer_Token = ""

ACCESS_TOKEN = ""
ACCESS_SECRET = ""



auth = tweepy.OAuthHandler(API_KEY, API_Secret_Key)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

 
hashtag = '#covid19'

TCP_IP = 'localhost'
TCP_PORT = 9001




def preprocessing(tweet):

    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)

    return regrex_pattern.sub(r'',tweet)


def getTweet(status):
    
    # You can explore fields/data other than location and the tweet itself. 
    # Check what else you could explore in terms of data inside Status object

    tweet = ""
    location = ""
    created_at = ""

    location = status.user.location
    created_at = status.created_at
    
    if hasattr(status, "retweeted_status"):  # Check if Retweet
        try:
            tweet = status.retweeted_status.extended_tweet["full_text"]
        except AttributeError:
            tweet = status.retweeted_status.text
    else:
        try:
            tweet = status.extended_tweet["full_text"]
        except AttributeError:
            tweet = status.text

    return location, preprocessing(tweet), created_at


def getUserInput():
    tags = []

    print("Enter the hashtags you want searched, delimit with ; (eg -> covid19;israel;marvel: ")
    t = input()

    tags_1 = t.split(";")

    for tag in tags_1:
        tags.append("#" + tag)

    return tags

tags = getUserInput()
print(tags)


# #create sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()



class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # print(status)
        location, tweet, created_at = getTweet(status)

        dt = created_at.strftime('%a %b %d %H:%M:%S %Y')

        if (location != None and tweet != None and created_at is not None):
            print(dt)
            tweetLocation = location + "::" + tweet + "::" + dt + "\n"
            conn.send(tweetLocation.encode('utf-8'))


        return True


    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)

myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
myStream.filter(track=tags, languages=["en"])
