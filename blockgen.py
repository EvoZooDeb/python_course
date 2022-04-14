#!/usr/bin/python3

import re
import sys

def digest(block):
  print(block)

def blocks(f):
    blocklines = []
    for line in f:
        if re.match(r'[0-9]+\s+[0-9]+', line):
            if blocklines:
                yield blocklines
            blocklines = [ line ]
        else:
            if blocklines:
                blocklines.append(line)
    if blocklines:
        yield blocklines

for block in blocks(sys.stdin):
    digest(block)
