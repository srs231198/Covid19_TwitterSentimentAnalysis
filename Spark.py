from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from geopy.geocoders import Nominatim
from textblob import TextBlob
import json
from elasticsearch import Elasticsearch
from datetime import datetime



TCP_IP = 'localhost'
TCP_PORT = 9001



def processTweet(tweet):

    # Here, you should implement:
    # (i) Sentiment analysis,
    # (ii) Get data corresponding to place where the tweet was generate (using geopy or googlemaps)
    # (iii) Index the data using Elastic Search 
    es = Elasticsearch(cloud_id="", http_auth=('elastic', ''))  
    
    tweetData = tweet.split("::")

    if len(tweetData) > 2:
        
        created_at = tweetData[2]
        text = tweetData[1]
        rawLocation = tweetData[0]

        doc = {}

        # (i) Apply Sentiment analysis in "text"

        # (ii) Get geolocation (state, country, lat, lon, etc...) from rawLocation

        print("\n\n=========================\ntweet: ", text)
        print("\nRaw location from tweet status: ", rawLocation)
        t = TextBlob(text)
        print("\n Sentiment : ", t.sentiment)
        print("\n Polarity  : ", t.sentiment.polarity)

        doc["Polarity"] = t.sentiment.polarity
        doc["Subjectivity"] = t.sentiment.subjectivity

        geolocator = Nominatim(user_agent="bts")
        l = geolocator.geocode(rawLocation, exactly_one=True, addressdetails=True)


        if l is not None:
            print("\nLocation: ", l.raw)
            print("\nLatitude", l.latitude)
            print("\nLongitude", l.longitude)
        
        doc["location"] = {"lat": l.latitude if l is not None else 0.0, "lon": l.longitude if l is not None else 0.0}
        doc["Address"] = l.raw['address'] if l is not None else {}
        

        if t.sentiment.polarity < 0:
            sentiment = "negative"
        elif t.sentiment.polarity == 0.0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        
        doc["message"] = text
        doc["sentiment"] = sentiment
        doc["date"] = datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y')
    
        #"polarity": t.sentiment.polarity,"subjectivity": t.sentiment.subjectivity,
        # (iii) Post the index on ElasticSearch or log your data in some other way
        es.index(index="bb-index",body=doc)

        print(doc)

        



# Pyspark
# create spark configuration
conf = SparkConf()
conf.setAppName('TwitterApp')
conf.setMaster('local[2]')

# create spark context with the above configuration
sc = SparkContext(conf=conf)

# create the Streaming Context from spark context with interval size 4 seconds
ssc = StreamingContext(sc, 4)
ssc.checkpoint("checkpoint_TwitterApp")

# read data from port 900
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)


dataStream.foreachRDD(lambda rdd: rdd.foreach(processTweet))


ssc.start()
ssc.awaitTermination()
