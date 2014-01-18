# -*- coding: utf-8 -*-

import json
import tweepy
import string
from random import choice

import midi

# decorator for tweet functions
def algorhythm(func):
  def tweet_music(tweet, midi):
    try:
      tweet = json.loads(tweet)
    except TypeError:
      print 'ERROR!'
      return True
    else:
      return func(tweet, midi)

  return tweet_music


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

if __name__ == '__main__':

  # build scale
  scale = midi.utils.build_scale(10, [0, 3, 5, 7, 9], min_note=10, max_note = 50)

  # build lookup of letters to notes
  lookup = {}
  az = [i for i in string.letters + string.digits]
  for i, a in enumerate(az):
    if i <= (len(scale)-1):
      lookup[a] = scale[i]

  # define function to play tweet
  @algorhythm
  def azAZ09(tweet, midi):
    if 'text' in tweet:
      text = tweet['text'].encode('utf-8', 'ignore').lower()
      print "< tweet > %s" % text
      for c in text:
        if c in lookup:
          note = lookup[c]
          midi.play_note(note, choice(range(50, 100, 1)), 0.5)

  m = TweetMusic(
    consumer_key = '',
    consumer_secret = '',
    access_key = '',
    access_secret = ''
  )

  m.run(term='ok', func=azAZ09)
