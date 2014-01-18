import string
from random import choice

from tweet_music import TweetMusic, midi, algorhythm

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
def az(tweet, midi):
  if 'text' in tweet:
    text = tweet['text'].encode('utf-8', 'ignore').lower()
    print "< tweet > %s" % text
    for c in text:
      if c in lookup:
        note = lookup[c]
        midi.play_note(note, choice(range(50, 100, 1)), 0.125)

m = TweetMusic(
  consumer_key = '',
  consumer_secret = '',
  access_key = '',
  access_secret = ''
)

m.run(term='ok', func=az)