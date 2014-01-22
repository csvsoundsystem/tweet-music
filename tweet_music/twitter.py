from console import log_style, log_img, log_gif
from language import Haiku
from music import Midi, midi_utils, constants
from speech import say, say_utils
from streams import TwitterStream, SocketStream
import time


haiku = Haiku()

rates = range(150, 200, 5)

twt_strm = TwitterStream(

)

def twt_id_to_attr(twt_id):
  twt_id = int(twt_id)

  # select voice
  voice = say_utils.VOICES[twt_id % len(say_utils.VOICES)]

  # select rate
  rate = rates[twt_id % len(rates)]

  # select markup
  markup = say_utils.COLOR_COMBOS[twt_id % len(say_utils.COLOR_COMBOS)]

  return voice, rate, markup

def on_twt(tweet):

  # initialize the cache
  twt_ids = []

  if 'text' in tweet:
    twt_id = tweet['id_str']
    if twt_id not in twt_ids:
      text = tweet['text'].encode('utf-8', 'ignore')
      hk = haiku.detect(text)
      if hk:
        voice, rate, markup = twt_id_to_attr(twt_id)
        img_url = tweet['user']['profile_image_url']
        log_img(img_url, format='url', width=30, height=35)
        say(hk, voice, rate, interactive=True, markup=markup)

      twt_ids.append(twt_id)

      # flush the cache
      if len(twt_ids) > 50:
        twt_ids = []

twt_strm.apply(['the'], on_twt)