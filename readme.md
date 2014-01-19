tweet_music @ => ♬
==================

`tweet_music` is a set of tools for creating and apply functions that create music via the twitter stream.

## Dependencies
`tweet_music` depends on `rtmidi` which can be downloaded [here](http://trac.chrisarndt.de/code/wiki/python-rtmidi). All other dependencies should be handled on install.

## Installation:
```
python setup.py install
```

## Example:
```python
"""

USAGE:
python az.py <channel> <duration>

EX:
python az.py 1 0.5

"""

from tweet_music import TweetMusic, midi, algorhythm
from tweet_music.midi.constants import music 

import string
from random import choice

# build scale
scale808 = midi.utils.build_scale(
  key = 'A', scale = music.SCALES['HARMONIC_MINOR_SCALE'], 
  min_note='A1', max_note = 'A7'
)

# build lookup of letters to notes
lookup = {}
az = [i for i in string.letters + string.digits]
for i, a in enumerate(az):
  if i <= (len(scale808)-1):
    lookup[a] = scale808[i]

# define function to play tweet
@algorhythm
def az(tweet, midi):
  if 'text' in tweet:
    text = tweet['text'].encode('utf-8', 'ignore')
    print "< tweet > %s" % text
    for c in text:
      if c in lookup:
        note = lookup[c]
        velocity = choice(range(70, 110, 5))
        midi.play_note(int(sys.argv[1]), note, velocity, float(sys.argv[2]))
# Initiatilize TweetMusic object by connecting to twitter.
if __name__ == '__main__':

  # Initiatilize TweetMusic object by connecting to twitter.
  tm = TweetMusic(
    consumer_key = '',
    consumer_secret = '',
    access_key = '',
    access_secret = ''
  )

  tm.run(term='ok', func=az)
```
