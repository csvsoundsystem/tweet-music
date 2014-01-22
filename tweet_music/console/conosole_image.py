#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import sys
import time
import base64
import StringIO

from image_utils import parse_b64_img, parse_url_img

class ConsoleImageError(Exception):
  pass

def log_img(img, format = "PIL", width=None, height=None, debug=False):
  
  # parse image
  img = _parse_img(img, format)

  # get original width and height
  orig_width = img.size[0]
  orig_height = img.size[1]

  # defautlt to original
  if width is None:
    width = orig_width
  if height is None:
    height = orig_height

  # try to speedup compiling
  try:
    (_rgb_to_xterm, _xterm_to_rgb) = _compile_speedup()
  except:
    if debug:
      print("WARNING: Failed to compile code, no speedup")
  frame = _get_frame(img, orig_width, orig_height, width, height)
  _print_frame(frame, width, height)


def log_gif(gif, width=None, height=None, debug=False):

  # parse image
  gif = _parse_img(gif, format)

  # get original width and height
  orig_width = gif.size[0]
  orig_height = gif.size[1]

  # defautlt to original
  if width is None:
    width = orig_width
  if height is None:
    height = orig_height

  # try to speedup compiling
  try:
    (_rgb_to_xterm, _xterm_to_rgb) = _compile_speedup()
  except:
    if debug:
      print("WARNING: Failed to compile code, no speedup")
  
  _iterate_frames(gif, orig_width, orig_height, width, height)


def _parse_img(img, format):
  format = format.upper()
  if format == 'PIL':
    return img
  elif format = 'URL':
    return parse_url_img(img)
  elif format = 'B64':
    return parse_b64_img(img)
  else:
    raise ConsoleImageError('"%s" is invalid. `format` must equal "PIL", "url", or "b64"' % format)


character = u'▄'
native = "_xterm256.c"

CUBE_STEPS = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
BASIC16 = ((0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
           (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
           (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
           (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255))

COLOR_TABLE = [_xterm_to_rgb(i) for i in xrange(256)]


def _xterm_to_rgb(xcolor):
  assert 0 <= xcolor <= 255
  if xcolor < 16:
    # basic colors
    return BASIC16[xcolor]
  elif 16 <= xcolor <= 231:
    # color cube
    xcolor -= 16
    return (CUBE_STEPS[(xcolor / 36) % 6],
            CUBE_STEPS[(xcolor / 6) % 6],
            CUBE_STEPS[xcolor % 6])
  elif 232 <= xcolor <= 255:
    # gray tone
    c = 8 + (xcolor - 232) * 0x0A
    return (c, c, c)

def _rgb_to_xterm(r, g, b):
  if r < 5 and g < 5 and b < 5:
      return 16
  best_match = 0
  smallest_distance = 10000000000
  for c in xrange(16, 256):
      d = (COLOR_TABLE[c][0] - r) ** 2 + \
          (COLOR_TABLE[c][1] - g) ** 2 + \
          (COLOR_TABLE[c][2] - b) ** 2
      if d < smallest_distance:
          smallest_distance = d
          best_match = c
  return best_match

def _print_pixel(rgb1,rgb2):
  c1 = _rgb_to_xterm(rgb1[0], rgb1[1],rgb1[2])
  c2 = _rgb_to_xterm(rgb2[0], rgb2[1],rgb2[2])
  sys.stdout.write('\x1b[48;5;%d;38;5;%dm' % (c1, c2))
  sys.stdout.write(character)

def _get_frame(im, orig_width, orig_height, width, height):
  if width!=orig_width or height!=orig_height:
    return im.resize((width,height), Image.ANTIALIAS).convert('RGB')
  else:
    return im.convert('RGB')

def _print_frame(im, width, height):
  for y in range(0,height-1,2):
    for x in range(width):
      p1 = im.getpixel((x,y))
      p2 = im.getpixel((x,y+1))
      _print_pixel(p1, p2)
    print('\x1b[0m')

def _iterate_frames(im, orig_width, orig_height, width, height):
  
  while True:
    frame = _get_frame(im, orig_width, orig_height, width, height)
    _print_frame(frame, width, height)
    try:
        im.seek(im.tell()+1)
    except EOFError:
        break

def _compile_speedup():
  
  import os
  import ctypes
  
  from os.path import join, dirname, getmtime, exists, expanduser
  
  library = join(dirname(__file__), '_xterm256.so')
  # library = expanduser('~/.xterm256.so')
  sauce = join(dirname(__file__), native)

  if not exists(library) or getmtime(sauce) > getmtime(library):
    build = "gcc -fPIC -shared -o %s %s" % (library, sauce)
    assert os.system(build + " >/dev/null 2>&1") == 0

  xterm256_c = ctypes.cdll.LoadLibrary(library)
  xterm256_c.init()
  
  def _xterm_to_rgb(xcolor):
    res = xterm256_c._xterm_to_rgb_i(xcolor)
    return ((res >> 16) & 0xFF, (res >> 8) & 0xFF, res & 0xFF)

  return (xterm256_c._rgb_to_xterm, _xterm_to_rgb)



