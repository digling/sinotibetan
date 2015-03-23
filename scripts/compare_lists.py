# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-23 14:23
# modified : 2015-03-23 14:23
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-03-23"

from lingpy import *
import sys

list1 = csv2list(sys.argv[1])
header1 = list1[0]
list2 = csv2list(sys.argv[2])
header2 = list2[0]

gidx1 = header1.index('GLOSS')
gidx2 = header2.index('GLOSS')


def find_break(word):
    
    out = ''
    for char in word:
        if char not in '([{,;':
            out += char
        else:
            break
    return out.strip()

matches = {}
for i,a in enumerate(list1[1:]):
    for j,b in enumerate(list2[1:]):
         
        wA = find_break(a[gidx1])
        wB = find_break(b[gidx2])

        if wA == wB or wA in b[gidx2].split(' ') or wB in a[gidx1].split(' '):
            try:
                matches[i+1] += [(wA,a[gidx1],j,wB,b[gidx2])]
            except KeyError:
                matches[i+1] = [(wA,a[gidx1],j,wB,b[gidx2])]
        else:
            if not i+1 in matches:
                matches[i+1] = []

for m in matches:
    if len(matches[m]) > 1:
        dst = []
        for k in range(len(matches[m])):
            dst += [edit_dist(matches[m][k][0], matches[m][k][4],
                normalized=True)]
        mind = min(dst)
        midx = dst.index(mind)
        matches[m] = [matches[m][midx]]

idx = 1
count = 0
for k in matches:
    if matches[k]:
        for line in matches[k]:
            print(k,'\t',line[1],'\t',line[2],'\t',line[4])
    else:
        print(k,'\t',list1[k][gidx1],'\t','?\t?')
        count += 1
            


