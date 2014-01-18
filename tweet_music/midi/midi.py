# -*- coding: utf-8 -*-

import time
import rtmidi
import sys

from utils import note_to_midi, root_to_midi, chord_to_midi
from constants.midi_messages import NOTE_ON, NOTE_OFF

class Midi(object):
  
  def __init__(self):
    self.out = rtmidi.MidiOut()
    available_ports = self.out.get_ports()
    if available_ports:
        self.out.open_port(0)
    else:
        self.out.open_virtual_port("My virtual output")

  def play_note(self, note, velocity, duration):
    
    # convert note
    note = note_to_midi(note)

    # validate velocity
    velocity = self._validate_velocity(velocity)

    # note on
    self.out.send_message([NOTE_ON, note, velocity])

    # pause
    time.sleep(duration)

    # note off
    self.out.send_message([NOTE_OFF, note, velocity])

  def play_chord(self, root, name, velocity, duration):
    
    # build chord
    root = note_to_midi(root)
    intervals = chord_to_midi(name)
    notes = [root + i for i in intervals if (root + i) < 128]

    # validate velocity
    velocity = self._validate_velocity(velocity)

    # notes on
    for n in notes:
      self.out.send_message([NOTE_ON, n, velocity])

    time.sleep(duration)

    # notes off
    for n in notes:
      self.out.send_message([NOTE_OFF, n, velocity])

  def _validate_velocity(self, velocity):
    if velocity > 127: 
      return 127
    elif velocity < 1 : 
      return 1
    else:
      return velocity
