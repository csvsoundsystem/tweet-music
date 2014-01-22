#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import tweepy
import re, time, string, random, json, yaml
from collections import defaultdict
from nltk.corpus import cmudict
import time

def gen_n2w():
  # number to word lookup
  # generate number lookup for 0 - 99
  n2w = "zero one two three four five six seven eight nine".split()
  n2w.extend("ten eleven twelve thirteen fourteen fifteen sixteen".split())
  n2w.extend("seventeen eighteen nineteen".split())
  n2w.extend(tens if ones == "zero" else (tens + " " + ones) 
    for tens in "twenty thirty forty fifty sixty seventy eighty ninety".split()
    for ones in n2w[0:10])

class Haiku(object):
  def __init__(self):

    # generate n2w 
    self.n2w = gen_n2w()

    # syllable dict
    self.cmu = cmudict.dict()


  def detect(self, text, format = None):

    # tokenize text
    words = self._clean_and_tokenize(text)

    if words:

      # attempt to map words to syllables
      word_dict = self._lookup_syllables(words)

      # check if it's a haiku
      if word_dict and self._is_proper_haiku(word_dict):

        # return the formatted version
        return self._format_haiku(word_dict, format)

  def _number_of_syllables(self, word):
    return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu[word]]

  def _remove_urls(self, string):
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    return re.sub(pattern, ' ', string)

  def _clean_and_tokenize(self, text):
    tweet = text.decode('utf-8', 'ignore')

    # remove urls
    text = self._remove_urls(text)
    
    # ignore texts with @s, RT's and MT's and numbers greater than 3 digits
    if re.search(r'@|#|MT|RT|[0-9]{3,}', text):
      return None

    # swap ampersand with and
    text = re.sub("&", " and ", text)

    # remove punctuation,  strip and lower text
    text = text.translate(string.maketrans("",""), string.punctuation).strip().lower()

    # split text into a list of words
    words = [w.strip() for w in text.split() if w != '' and w is not None]

    # replace two-digit numbers with words
    words = [self.n2w[int(w)] if re.search(r"0-9{,2}", w) else w for w in words]

    return words

  def _lookup_syllables(self, words):

    # filter our text which will definitely not work
    n_syllables = []
    clean_words = []

    for word in words:
      try:
        n_syllable = self._number_of_syllables(word)[0]
      except KeyError:
        return None
      if n_syllable > 7:
        return None
      else:
        n_syllables.append(n_syllable)
        clean_words.append(word.strip())

    return {"words" : clean_words, "syllables" : n_syllables }


  def _is_proper_haiku(self, word_dict):

    # make sure haikus have the proper number of syllables
    if  sum(word_dict['syllables']) != 17:
      return False

    # make sure lines break at 5 and 12 by counting up syllabes
    syllable_cum_sum = []
    syllables_so_far = 0

    for syllable in word_dict['syllables']:
      syllables_so_far += syllable
      syllable_cum_sum.append(syllables_so_far)

    if 5 in syllable_cum_sum and 12 in syllable_cum_sum:
      return True
    else:
      return False

  def _format_haiku(self, haiku_dict, format):
    words = haiku_dict['words']
    syllables = haiku_dict['syllables']
    syllable_count = 0
    haiku = ''
    delim = ", \r\n"
    for i, word in enumerate(words):
      if syllable_count == 5 or syllable_count == 12:
        haiku = haiku.strip() 
        haiku += delim
      syllable_count += syllables[i]
      haiku += word.strip() + " "
    if format == "list":
      return [ l.strip() for l in haiku.split(delim)]
    else:
      return haiku.strip()



