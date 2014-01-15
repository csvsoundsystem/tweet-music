import json
import tweepy
import os
 
consumer_key = 'luNYqynZjp26awakJaGing'
consumer_secret = 'o2VSEZrXzI6L8kpV9tlN2IOdxv2koAOJpUwgQTkAZA'
access_key = '432708845-PuDX6SOfho6hSITCCowFOAuauR7PU4oMeO3cYZB8'
access_secret = 'JMp6lmLTnYF42X0957vg2dSuic23CrbhqsSBCE865KU'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
  def __init__(self, api):
    self.api = api
    super(tweepy.StreamListener, self).__init__()

  def on_data(self, tweet):
    data = json.loads(tweet)
    print data['text']

  def on_error(self, status_code):
    return True # Don't kill the stream

  def on_timeout(self):
    return True # Don't kill the stream

if __name__ == '__main__':
  stream = tweepy.streaming.Stream(auth, StreamListener(api))
  os.system('say ' + stream.filter(track=['poop']) + ' &')