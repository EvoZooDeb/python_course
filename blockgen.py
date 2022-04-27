#!/usr/bin/python3

import re
import sys
import json

def clean(block):
    result = []
    for line in block:
        line = line.strip()
        line = re.sub(r'^[0-9]+\s*', '', line)
        if re.fullmatch(r'^[0-9]+$', line):
            continue
        if line:
            result.append(line)
    return result

def blocks(f):
    blocklines = []
    for line in f:
        if re.match(r'[0-9]', line):
            if blocklines:
                yield clean(blocklines)
            blocklines = [ line ]
        else:
            if blocklines:
                blocklines.append(line)
    if blocklines:
        yield clean(blocklines)

def digest(block):

    # Eurytop|Stenotop|Ubiquist|Synanthrop|Coprophil|eurytop|Kaltstenotop
    # "":  xxx - xxx - xxx REGEXP: '^([a-zA-Z]+ — )+[a-zA-Z]+$'

    info        = {}
    firstline   = True
    label       = ''
    info[label] = ''

    for line in block:

        if firstline:
            spid, spname   = line.split(' ', 1)
            info['spid'  ] = spid
            info['spname'] = spname
            firstline      = False
        else:
            if re.match(r'H:', line):
                label       = 'H:'
                info[label] = ''
            elif re.match(r'Na:', line):
                label       = 'Na:'
                info[label] = ''
            elif re.match(r'Ni:', line):
                label       = 'Ni:'
                info[label] = ''
            info[label] += ' '+line

    found = re.search(r' ([a-zA-Z]+ [—-] )+[a-zA-Z]+$', info[''])
    if found:
      print(found.start(), info[''])
    #print(json.dumps(info, indent=2, ensure_ascii=False))
    #print('')

for block in blocks(sys.stdin):
#    for i in block:
#        print(i)
#    print('')
    digest(block)
