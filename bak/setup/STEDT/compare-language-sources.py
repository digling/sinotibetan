# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-11 10:18
# modified : 2015-03-11 10:18
"""
Compare languages in three major sources in STEDT.
"""

__author__="Johann-Mattis List"
__date__="2015-03-11"

from lingpy import *

sources = ['zmyyc', 'tbl', 'gem-cnl']

langs = {}
for s in sources:

    data = csv2list(
            'sources/'+s+'.languages.tsv',
            strip_lines=False
            )
    header = ['iso', 'name', 'short_name', 'group','records','inventory']
    
    for line in data:
        
        tmpd = dict(zip(header,line))
        try:
            langs[line[1]][s] = tmpd
        except KeyError:
            langs[line[1]] = {s:tmpd}

all_sources = []
for i,l in enumerate(langs):
    #print(i+1,'\t',l,'\t',','.join(langs[l].keys()))

    all_sources += [(i+1,l,len(langs[l]), tuple(langs[l].keys()))]

for i,(a,b,c,d) in enumerate(sorted(all_sources, key=lambda x: (x[2],x[1]))):
    print(i+1,'\t',b,'\t',c,'\t','/'.join(d))
            
import json

with open('meta_all_sources.json', 'w') as f:
    f.write(json.dumps(langs,indent=2))

