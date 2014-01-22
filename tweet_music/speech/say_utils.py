#!/usr/bin/env python
# -*- coding: utf-8 -*-

VOICES = ["Alex", "Bruce", "Fred", "Ralph", "Kathy", "Vicki", "Victoria", "Princess", "Agnes", "Junior"]

MARKUP = ['bold', 'smul', 'setaf 1']
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

COLOR_COMBOS = ["%s/%s" % (fg, bg) for fg in COLORS for bg in COLORS if fg != bg]