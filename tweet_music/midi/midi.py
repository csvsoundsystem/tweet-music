import time
import rtmidi

from noteconstants import note_to_midi, root_to_midi, chord_to_midi
from midiconstants import *

class Midi(object):
  
  def __init__(self):
    self.midiout = rtmidi.MidiOut()
    available_ports = self.midiout.get_ports()
    if available_ports:
        self.midiout.open_port(0)
    else:
        self.midiout.open_virtual_port("My virtual output")

  def play_note(self, note, velocity, duration):
    
    # convert note
    note = note_to_midi(note)

    # note on
    self.midiout.send_message([NOTE_ON, note, velocity])

    # pause
    time.sleep(duration)

    # note off
    self.midiout.send_message([NOTE_OFF, note, velocity])

  def play_chord(self, root, name, velocity, duration):
    
    # build chord
    root = note_to_midi(root)
    intervals = chord_to_midi(name)
    notes = [root + i for i in intervals if (root + i) < 128]

    # notes on
    for n in notes:
      self.midiout.send_message([NOTE_ON, n, velocity])

    time.sleep(duration)

    # notes off
    for n in notes:
      self.midiout.send_message([NOTE_OFF, n, velocity])

if __name__ == '__main__':
  m = Midi()
  m.play_chord('G4', 'maj', 60, 5)

