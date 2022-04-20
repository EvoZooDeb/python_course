#!/usr/bin/python3

import re
import sys

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

list_of_row_info = []
for block in blocks(sys.stdin):
    dict_of_row_info = {}
    for i in range(1, len(block)+1):
      if block[i-1] == block[0]:
       row_info = re.split(' ', block[0], 2)
       dict_of_row_info['row_number'] = row_info[0]
       dict_of_row_info['id'] = row_info[1]
       dict_of_row_info['species'] = row_info[2]
      else:
         if block[i-1] == block[1]:
           row_info = re.sub(r'[0-9]+	','', block[1])
           dict_of_row_info['Weite_und_jahreszeitlich_bedingter_Wechsel_des_Monotops+besondere_Ansprüche'] = row_info
         else:
             if block[i-1] == block[2]:
                 list_to_append = []
                 if len(block) > 3:
                     for j in range(3, len(block)):
                         #list_to_append.insert(0, '')
                         list_to_append.append(block[j])
                 #print('-----------LISTTOAPPEND------------')
                 #print(list_to_append)
                 #print('-----------LISTTOAPPEND------------')
                 block[2] = block[2] + ''.join(list_to_append)
                 #print('-----------BLOCK2------------')
                 #print(block[2])
                 #print('-----------BLOCK2------------')
                 block[2] = re.sub(r'[0-9]+	', '', block[2])
                 row_info = re.split(r'H:|Ni:|Na:', block[2])
                 if len(row_info) > 1:
                     dict_of_row_info['Habitat'] = row_info[1]
                     if len(row_info) > 2:
                         dict_of_row_info['Nische']  = row_info[2]
                         if len(row_info) > 3:
                             dict_of_row_info['Nahrung'] = row_info[3]
                 #print(dict_of_row_info)
                 #print('-----------ROWINFO------------')
                 #print(row_info)
                 #print('-----------ROWINFO------------')
    list_of_row_info.append(dict_of_row_info)
    
for dictionary in list_of_row_info:
    for key, value in dictionary.items():
        print(key, ':', value)
    print('------------------------------------------------------------------------NEXT_ENTRY------------------------------------------------------------------------')
    print('')

    

# Print block helyett digest block ? Vmi függvény ami feldolgozza az adot blockot. 0 index lista elemben fejrész azonosító kóddal, utána latin név stb.
#def digest_blocks(b):
#    block_info = {}
#    for block in blocks(sys.stdin):
#        if re.match(r'\', \'', sep):
    
    
