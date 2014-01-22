#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipes import quote
import subprocess

def say(text, voice = 'Kathy', rate = 180, chorus=False, interactive = True, markup = None):
  
  args = (quote(str(voice.title())), quote(str(rate)), quote(str(text)))
  cmd = ['say', '-v', args[0], '-r', args[1], args[2]]

  if interactive:
    if markup:
      cmd += ['--interactive=%s' % quote(markup)]
    else:
      cmd += ['--interactive']

  if chorus:
    subprocess.Popen(cmd, shell=False)
  else:
    subprocess.call(cmd, shell=False)