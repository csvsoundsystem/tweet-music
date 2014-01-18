# -*- coding: utf-8 -*-

import json
import tweepy
import string
from random import choice

import midi

# decorator for apply midi creation functions to tweet functions
def algorhythm(func):
  def run_algorhythm(tweet, midi):
    try:
      tweet = json.loads(tweet)
    except TypeError:
      print 'ERROR!'
      return True
    else:
      return func(tweet, midi)
  return run_algorhythm


class OnTweet(tweepy.StreamListener):
  """
  Generic class for applying music function to twitter stream
  """
  def __init__(self, api, func):
    self.api = api
    self.func = func
    self.midi = midi.Midi()
    super(tweepy.StreamListener, self).__init__()

  def on_data(self, tweet):
    self.func(tweet, self.midi)

  def on_error(self, status_code):
    return True # Don't kill the stream

  def on_timeout(self):
    return True # Don't kill the stream

class TweetMusic:
  """
  Connect to twitter and 
  """
  def __init__(self, **kwargs):
    
    # connect to twitter
    ck = kwargs.get('consumer_key')
    cs = kwargs.get('consumer_secret')
    ak = kwargs.get('access_key')
    asec = kwargs.get('access_secret')
    self.auth = tweepy.OAuthHandler(ck, cs)
    self.auth.set_access_token(ak, asec)
    self.api = tweepy.API(self.auth)

  def run(self, term, func):
    stream = tweepy.streaming.Stream(self.auth, OnTweet(self.api, func))
    print "< streaming > %s" % term
    stream.filter(track=[term])