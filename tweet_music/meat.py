from console import log_style, log_img, log_gif
from console.text_utils import wrap_text
from language import Haiku
from music import Midi, midi_utils
from music.constants import theory
from speech import say, say_utils
from streams import TwitterStream, SocketStream
import time
import string
from random import choice
import re

m = Midi()

# build scale
scale = midi_utils.build_scale(
  key = 'E', scale =[0,4,7,9,14,19], 
  min_note='E1', max_note = 'A5'
)

# build lookup of letters to notes
lookup = {}
az = [i for i in string.letters + string.digits]
for i, a in enumerate(az):
  if i <= (len(scale)-1):
    lookup[a] = scale[i]

chords = [
  ('E3', 'sus'), 
  ('A3', 'maj9_no_fifth'), 
  ('F#3', 'power'), 
  ('B3', 'maj'), 
  ('C#3', 'min'),
  ('E3', 'sus2'),
  ('A3', 'power')
]

rates = range(150, 200, 5)

def parse_meat(*args):
  
  resp = args[0]
  data = dict(
    message = resp['chat']['value']['message'].encode('utf-8'),
    b64_gif = resp['chat']['value']['media'],
    fingerprint = resp['chat']['value']['fingerprint'].encode('utf-8')
  )
  return data

def fingerprint_to_attr(fingerprint):
  fingerprint = int(re.sub(r'[a-z\-]+', '', fingerprint.lower()).strip())


  # select voice
  voice = say_utils.VOICES[fingerprint % len(say_utils.VOICES)]

  # select rate
  rate = rates[fingerprint % len(rates)]

  # select markup
  markup = say_utils.COLOR_COMBOS[fingerprint % len(say_utils.COLOR_COMBOS)]

  return voice, rate, markup

def on_meat(meat):
  meat = parse_meat(meat)
  msg = meat['message']

  voice, rate, markup = fingerprint_to_attr(meat['fingerprint'])

  log_gif(meat['b64_gif'], format='b64', width = 30, height = 20)
  chord = choice(chords)
  m.play_chord(channel=1, root=chord[0], name=chord[1], velocity = 80, duration = 0.1)
  log_style(wrap_text(msg, 30), 'fg_cyan', 'bg_red')
      



meat_strm = SocketStream(address='https://chat.meatspac.es', port=443)
meat_strm.apply(on_meat)
  