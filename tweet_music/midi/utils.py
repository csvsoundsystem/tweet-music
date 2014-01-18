# -*- coding: utf-8 -*-

from constants import music

def note_to_midi(n):
  if isinstance(n, basestring):
    return music.NOTES[n]
  elif isinstance(n, int):
    return n

def root_to_midi(n):
  if isinstance(n, basestring):
    return music.ROOTS[n]
  elif isinstance(n, int):
    return n

def chord_to_midi(name):
  return music.CHORDS[name]

def build_scale(key, scale, min_note=0, max_note=128):
  
  # convert args    
  key = root_to_midi(key)
  min_note = note_to_midi(min_note)
  max_note = note_to_midi(max_note)

  # build scale
  s = [s + key for s in scale]

  # define
  return [ 
    x + (12 * j)
    for j in range(12)
    for x in s
    if x + (12 * j) >= min_note and x + (12 * j) <= max_note
  ]