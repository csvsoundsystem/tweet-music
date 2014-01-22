#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap

def wrap_text(text, max_width):
  """
  wrap message to set width
  """
  lines = textwrap.wrap(text, max_width)

  # return single line
  if len(lines)==1:

    text = lines[0].strip()

    # don't pad posts that are the max_width
    if len(text) == max_width:                                                         

      return text

    # pad posts that aren't wider than image
    else:

      fill = " " * (max_width - len(text))
      text += fill
      return text

  # break lines
  else:

    wrapped_lines = []

    for i, line in enumerate(lines):

      line = line.strip()
      fill = " " * (max_width - len(line))
      wrapped_lines.append(line + fill)
      
    return "\r\n".join(wrapped_lines)

STYLES = dict(
  bold = '\033[1m',
  underscore = '\033[4m',
  blink = '\033[5m',
  reverse = '\033[7m',
  concealed = '\033[7m',

  fg_black = '\033[30m',
  fg_red = '\033[31m',
  fg_green = '\033[32m',
  fg_yellow = '\033[33m',
  fg_blue = '\033[34m',
  fg_magenta = '\033[35m',
  fg_cyan = '\033[36m',
  fg_white = '\033[37m',

  bg_black = '\033[40m',
  bg_red = '\033[41m',
  bg_green = '\033[42m',
  bg_yellow = '\033[43m',
  bg_blue = '\033[44m',
  bg_magenta = '\033[45m',
  bg_cyan = '\033[46m',
  bg_white = '\033[47m'    
)