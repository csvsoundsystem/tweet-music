#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import tweepy

class TwitterStreamAuthError(Exception):
  pass

class _OnTweet(tweepy.StreamListener):
  """
  Generic class for applying function to twitter stream
  """
  def __init__(self, api, func):
    self.api = api
    self.func = func
    super(tweepy.StreamListener, self).__init__()

  def on_data(self, tweet):
    try:
      tweet = json.loads(tweet)
    except ValueError:
      return None
    self.func(tweet)

  def on_error(self, status_code):
    return True # Don't kill the stream

  def on_timeout(self):
    return True # Don't kill the stream

class TwitterStream(object):
  """
  Connect to twitter and 
  """
  def __init__(self, **kwargs):
    
    # check for existence of args
    req = ['consumer_key', 'consumer_secret', 'access_key', 'access_secret']
    missing = [r for r in req if r not in kwargs]
    if len(missing) > 1:
      raise TwitterStreamAuthError("\nTweetMusic is missing these twitter api credentials: %s" % ", ".join(missing))
    
    # validate args
    args_test = [True for r in req if kwargs.get(r)=='' or kwargs.get(r) is None]
    if any(args_test):
      raise TwitterStreamAuthError('\n%d of your api credentials are empty' % len(args_test))

    # extract args
    ck = kwargs.get('consumer_key')
    cs = kwargs.get('consumer_secret')
    ak = kwargs.get('access_key')
    asec = kwargs.get('access_secret')

    # conenct to twitter
    self.auth = tweepy.OAuthHandler(ck, cs)
    self.auth.set_access_token(ak, asec)
    self.api = tweepy.API(self.auth)

  def apply(self, terms, func):
    stream = tweepy.streaming.Stream(self.auth, _OnTweet(self.api, func))
    stream.filter(track=terms)
