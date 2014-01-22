#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipes import quote
import subprocess

def say(text, voice, rate, interactive=, chorus=True):
  
  args = (quote(str(voice)), quote(str(rate)), quote(str(text_to_speak)))
  cmd = ['say', '-v', args[0], '-r', args[1], args[2]]

  if chorus:
    subprocess.Popen(cmd, shell=False)
  else:
    subprocess.call(cmd, shell=False)