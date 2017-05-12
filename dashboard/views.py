from django.shortcuts import render
from rest_framework.views import APIView
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import re
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
import json
from pymongo import MongoClient

# Create your views here.
def main(request):
    return render(request, 'index.html')

def tables_view(request):
    return render(request, 'tables.html')

def charts_view(request):
    return render(request, 'charts.html')

# list of restaurant from the db
LOOKUP_KEYWORDS = ["deltaairlines", "southwestairlines","jetblue","virginairlines"] # to be taken from the mongo DB
LOOKUP_KEYWORDS2 = ["deltaairlines"] # to be taken from the mongo DB
class AnalyzeTweet():

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        print("Polarity:"+str(analysis.sentiment.polarity))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

# tweet_analyzer = AnalyzeTweet()
# input_text = "This restaurant #pistahouse"
# print("Input:"+input_text+"\nSentiment:"+tweet_analyzer.get_tweet_sentiment(input_text))
# sys.exit()

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('twitter_data.json', 'a') as f:
                f.write(data)
                tweet_obj = json.loads(data)
                tweet = tweet_obj['text']
                print("NEW TWEET: "+str(tweet))
                # sentiment = tweet_analyzer.get_tweet_sentiment(tweet)
                airline = ""
                # print("Sentiment: "+str(sentiment))
                # get restaurant name from the text
                for rest in LOOKUP_KEYWORDS:
                    if rest in tweet:
                        airline = rest
                print("Airline: "+airline)

                return True
        except BaseException as e:
            print("Error on_data: " % str(e))
        return True

    def on_error(self, status):
        print("Error in streaming!!")
        print(status)
        return True

class get_tweets(APIView):
    def get(self, request):
        consumer_key = "KYS0m11ML0WWuftNvjdaKF7iR"
        consumer_secret = "hKszS7x6pmkblS4iIa6Z5UkNpogucRK45T81T5DRoStmxn2a6y"
        access_token = "84014050-tgU5RY2ekrdRrQh4xVcZzuTHdbIimZ3SsFjobEn1J"
        access_token_secret = "SKtdtX1856iCTWk1UVARjLT3ObR3OGvnuIAiVHiv6U7uT"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # tweet_analyzer = AnalyzeTweet()

        # Below code to print the tweet matching the desired keyword.
        public_tweets = api.home_timeline()
        for keyword in LOOKUP_KEYWORDS2:
            cricTweet = tweepy.Cursor(api.search, q=keyword).items()
            print("======================"+keyword)
            i = 0
            for tweet in cricTweet:
                if i >= 6:
                    break
                else:
                    i += 1
                print("------")
                print "Created at: ",tweet.created_at
                print "Tweet: ",tweet.text
                print "lang:", tweet.lang
                print "geo:", tweet.geo
                try:
                    print "place country name:", tweet.place.country
                    print "place name:", tweet.place.name
                except:
                    print "No place found"
                # print "User:", tweet.user
                print "User Location:", tweet.user.location
                print "User name:", tweet.user.name