# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-15 13:01
# modified : 2015-04-15 13:01
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-04-15"

from lingpyd import *
from lingpyd.meaning.colexification import *
import sys

if 'precompile' in sys.argv:
    wl = Wordlist('tbl.tsv')
    
    subset = csv2list('tbl_vs_stdb-new.tsv')
    gloss2sub = {}
    for line in subset[1:]:
    
        gloss2sub[line[4]] = line[1]
    
    wl.add_entries('conceptid', 'srcid', lambda x: x.split('.')[0])
    idxs = {}
    for k in wl:
        
        cid = wl[k,'conceptid']
        if cid in gloss2sub:
            if ''.join([x for x in wl[k,'reflex'] if x not in '*-?-']):
                idxs[k] = '1'
            else:
                idxs[k] = '0'
        else:
            idxs[k] = '0'

    wl.add_entries('check', idxs, lambda x: x)

    print("writing data to file")
    wl.output('tsv', filename='tbl_colx', subset=True, rows=dict(check="== '1'"))
    #rows=dict(ID="in "+str(idxs)))

print('starting colex analysis')
wl = Wordlist('tbl_colx.tsv')

G = colexification_network(wl, entry='reflex')

for a,b,d in sorted(G.edges(data=True), key=lambda x:x[2]['word_weight']):

    print('{0:30}  <=> {1:30} ({2})'.format(a,b,d['word_weight']))

nodes,edges = evaluate_colexifications(G)

parts = partition_colexifications(G, weight='word_weight')

