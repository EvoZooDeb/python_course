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

def line2digest(info):

    # Eurytop|Stenotop|Ubiquist|Synanthrop|Coprophil|eurytop|Kaltstenotop|Mycetophil
    # "":  xxx - xxx - xxx REGEXP: '^([a-zA-Z]+ — )+[a-zA-Z]+$'

    line2 = info[''].strip()
    firstword, _ = line2.split(' ', 1) if ' ' in line2 else (line2, '')
    if firstword.lower() in [ 'eurytop', 'stenotop', 'ubiquist', 'synanthrop', 'coprophil', 'kaltstenotop', 'mycetophil' ]:
        return

    found = re.search(r' (eurytop|stenotop|ubiquist|synanthrop|coprophil|kaltstenotop|mycetophil) [—-] ', line2.lower())
    #found = re.search(r' ([a-zA-Z]+ [—-] )+[a-zA-Z]+$', line2)
    if found and found.start() > 0:
        info['spname'] += line2[:found.start()]
        info[''      ]  = line2[found.start():]
    else:
        info['spname'] += line2
        info[''      ]  = ''

def digest(block):

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

    line2digest(info)

    for key in info.keys():
        info[key] = info[key].strip()
        if key in [ 'H:', 'Na:', 'Ni:' ]:
            _, info[key] = info[key].split(' ', 1)

    return info

dataset = []
for block in blocks(sys.stdin):
    dataset.append(digest(block))

print(json.dumps(dataset, ensure_ascii=False, indent=2))
