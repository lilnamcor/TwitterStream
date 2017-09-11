import sys
import json
import tweepy
import time
import sys
from collections import Counter
from nltk.corpus import wordnet as wn
from operator import attrgetter

from listener import CustomStreamListener

# use your own combination of keys
consumer_key = 'SHfhYGKNHycCDheksL2fGzL8F'
consumer_secret = '58QNYoDgzbsrZRCzTwjJrYZRW1H2JzaDAPyi9p8vDwUSDHVG64'
access_key = '838654442-gYpAL7OOqiCZe0LjnnQ0KsDAIqubcSH8q0ZjT6dO'
access_secret = 'xV9vmlgAnTT9UQAA0k3BhSxpM4D9sfuP1qfa23qlxx1jY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

try:
    n = int(sys.argv[1])
except:
    n = 5
print 'Running with N = %s' % n
sapi = tweepy.streaming.Stream(auth, CustomStreamListener(n))
sapi.filter(track=['a', 'the', 'i', 'but', '.'], languages=['en'])
