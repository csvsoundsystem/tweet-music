#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import base64
import urllib2 as urllib
import io

def parse_b64_img(b64):
  # format string
  if "base64," in b64:
    b64 = b64.split('base64,')[1]

  # pad string
  b64 += "=" * ((4 - len(b64) % 4) % 4)

  # decode string
  data = base64.b64decode(b64)

  # read in encoded data
  f = StringIO.StringIO(data)

  # get original height and width
  return Image.open(f)

def parse_url_img(img_url):
  fd = urllib.urlopen(img_url)
  image_file = io.BytesIO(fd.read())
  return Image.open(image_file)