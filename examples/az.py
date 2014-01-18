from tweet_music import TweetMusic, midi, algorhythm
from tweet_music.midi.constants import music 

import string
from random import choice

# build scale
scale = midi.utils.build_scale(
  'E', music.SCALES['GYPSY_SCALE'], 
  min_note='E3', max_note = 'E9'
)

# build lookup of letters to notes
lookup = {}
az = [i for i in string.letters + string.digits]
for i, a in enumerate(az):
  if i <= (len(scale)-1):
    lookup[a] = scale[i]

# define function to play tweet
@algorhythm
def az(tweet, midi):
  if 'text' in tweet:
    text = tweet['text'].encode('utf-8', 'ignore')
    print "< tweet > %s" % text
    for c in text:
      if c in lookup:
        note = lookup[c]
        velocity = choice(range(50, 100, 1))
        midi.play_note(note, velocity, 0.125)

# Initiatilize TweetMusic object by connecting to twitter.
m = TweetMusic(
  consumer_key = '',
  consumer_secret = '',
  access_key = '',
  access_secret = ''
)

m.run(term='ok', func=az)