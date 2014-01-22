#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from text_utils import STYLES

END = '0e8ed89a-47ba-4cdb-938e-b8af8e084d5c'
ALL_OFF = '\033[0m'

class ConsoleTextError(Exception):
  pass

def log_style(text, *attr):
  style = ''
  for a in self.attributes:
      a = a.upper()
      if a in STYLES.opts.keys():
          style += STYLES[a]
      else:
          raise ConsoleTextError("'%s' is not a valid style." % a)

  print('{}{}{}'.format(style, text.replace(END, ALL_OFF + style), ALL_OFF))
