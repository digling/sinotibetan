# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-22 20:37
# modified : 2015-04-22 20:37
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-04-22"

from lingpyd import *

match = csv2list('matches.tsv')
tbl_concepts = csv2list('tbl_concepts.tsv')

tbl = dict([(a,b) for a,b in tbl_concepts[1:]])
concepts = {}
with open('stdb2tbl.tsv','w') as f:
    f.write('\t'.join(match[0][:-1])+'\n')
    for line in match[1:]:
        f.write('\t'.join(line[0:-3])+'\t'+tbl[line[-3]]+'\n')
        concepts[line[-3]] = line[1]

tbl = Wordlist('tbl.tsv')
for k in tbl:
    c = tbl[k,'concept']
    cid = tbl[k,'srcid'].split('.')[0]
    if cid in concepts:
        tbl[k][tbl.header['concept']] = concepts[cid]

tbl.output('tsv', filename='tbl.stdb.tsv', subset=True, rows=dict(
    concept = 'in '+str(sorted(concepts.values()))))
