# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-23 15:19
# modified : 2015-03-23 15:19
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-03-23"

from lingpy import *
import re

def fuzzy(word):

    if '[' in word:
        return word.split('[')[0].strip()
    else:
        return word

wl1 = csv2list('zmyyc_match.tsv')
wl2 = csv2list('tbl_match.tsv')

D = {}
for k in wl1:
    marker = ' ' if fuzzy(k[1]) == k[3] else '*' 
    try:
        D[k[0],k[1]] += [(marker,k[3],'zmyyc')]
    except:
        D[k[0],k[1]] = [(marker,k[3],'zmyyc')]

for k in wl2:
    marker = ' ' if fuzzy(k[1]) == k[3] else '*' 
    try:
        D[k[0],k[1]] += [(marker,k[3],'tbl')]
    except:
        D[k[0],k[1]] = [(marker,k[3],'tbl')]

with open('matches_tbl_zmyyc.tsv', 'w') as f:
    for k in sorted(D, key=lambda x: int(x[0])):
        f.write(k[0]+'\t'+k[1])
        for a,b,c in D[k]:
            if b == '?':
                b = '-'
            else:
                b = a+b
            f.write('\t'+b)

        f.write('\n')

    

