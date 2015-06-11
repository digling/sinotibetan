# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-11 10:39
# modified : 2015-03-11 10:39
"""
Retrieve gloss lists for STEDT sources.
"""

__author__="Johann-Mattis List"
__date__="2015-03-11"

from lingpy import *
from glob import glob

sources = glob('data/*.csv')


# get ambiguous words (based on noun-adjective-distinctions in TBL)
data = csv2list('data/TBL.csv', strip_lines=False)
agloss = {}


concepts = {}
for s in sources:

    data = csv2list(s, strip_lines=False)
    source = s.split('/')[1].strip('.csv')

    header = data[0]
    data = data[1:]

    for line in data:
        
        tmpd = dict(zip(header,line))
        
        if tmpd['gfn']:
            pos = tmpd['gfn'].replace('.','')
            try:
                agloss[tmpd['gloss']].add(pos)
            except KeyError:
                agloss[tmpd['gloss']] = set([pos])
        
        gloss = tmpd['gloss']
        
        try:
            concepts[gloss].add(source)
        except KeyError:
            concepts[gloss] = set([source])

ambs = {}
for g in agloss:
    if len(agloss[g]) > 1:
        ambs[g] = sorted(agloss[g])

count = 1
three_sources = []
two_sources = []
all_sources = []
for c in concepts:
    
    if c in ambs:
        marker = ','.join(sorted(ambs[c]))
    else:
        marker = ''

    entry = [c, marker, len(concepts[c]), ','.join(sorted(concepts[c]))]
    all_sources += [entry]

    if len(concepts[c]) > 1:
        two_sources += [entry]

    if len(concepts[c]) > 1:
        three_sources += [entry]
        if c in ambs:
            markerx = '*'
        else:
            markerx = ' '
        print(markerx,count,'\t',marker,'\t',c,'\t',len(concepts[c]), ','.join(sorted(concepts[c])))
        count += 1
    
with open('concepts_all_sources.tsv', 'w') as f:

    f.write('GLOSS\tAMBIGUITY\tCOVERAGE\tSOURCES\n')
    for line in sorted(all_sources, key=lambda x: (x[2],x[0])):
        f.write('\t'.join([str(x) for x in line])+'\n')

