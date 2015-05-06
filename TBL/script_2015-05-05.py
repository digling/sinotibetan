# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-05 16:16
# modified : 2015-05-05 16:16
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-05-05"

from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase


db = LexiBase('sinotibetan', dbase='sinotibetan.sqlite3',
        url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3'
        )

# get instances of tbl to modify the taxonomic units
tbl = Wordlist('tbl-update.tsv')
taxa = tbl.taxa

for k in db:
    if db[k,'concept'] == 'the child (young human':
        db[k][db.header['concept']] = 'the child (young human)'
        
for t in taxa:
    
    idxs = db.get_dict(taxon=t)['you [second person plural]']
    
    for idx in idxs:
        db[idx][db.header['concept']] = 'thou [second person singular]'

# now add missing entries
D = {}
D[0] = sorted([t for t in tbl.header if t in db.header], key=lambda x: db.header[x])

for i,t in enumerate(taxa):
    idxs = tbl.get_dict(taxon=t)['you [second person plural]']
    for idx in idxs:
        D[i+1] = [tbl[idx,h] for h in D[0]]

db.add_data(Wordlist(D))
db.renumber('concept')
db.create('sinotibetan', dbase='sinotibetan.sqlite3')
