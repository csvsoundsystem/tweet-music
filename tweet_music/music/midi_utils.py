#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import theory

class MidiUtilsError(object):
  pass

def note_to_midi(n):
  if isinstance(n, basestring):
    if n in theory.NOTES:
      return theory.NOTES[n]
    else:
      raise MidiUtilsError('"%s" is not a valid note.' % n)
  elif isinstance(n, int):
    return n

def root_to_midi(n):
  if isinstance(n, basestring):
    if n in theory.ROOTS:
      return theory.ROOTS[n]
    else:
      raise MidiUtilsError('"%s" is not a valid note.' % n)
  elif isinstance(n, int):
    return n

def chord_to_midi(name):
  if name in theory.CHORDS:
    return theory.CHORDS[name]
  else:
    raise MidiUtilsError('%s is not a valid chord name.' % name)

def build_scale(key, scale, min_note=0, max_note=127):
  
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