# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-05 16:04
# modified : 2015-05-05 16:04
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-05-05"

from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase

db = LexiBase('sinotibetan', dbase='sinotibetan.sqlite3',
        #url = 'http://tsv.lingpy.org/triples/sinotibetan.sqlite3'
        )

# get the concepts
concepts = [m[1] for m in csv2list('matches.tsv')]
# calculate coverage
corage = {}
ff = open('coverage.csv', 'w')
ff.write('DOCULECT\tPRESENT\tMISSING\tCOVERAGE\n')
for t in db.taxa:
    d = db.get_dict(taxon=t)
    present = [k for k in d if k in concepts]
    missing = [k for k in concepts if k not in d]
    c = len(present)
    corage[t] = (c,c/len(concepts),missing)
    if c < 220:
        print(t,c)
        
        with open('taxa/'+t+'.csv', 'w') as f:
            f.write('NUMBER\tWORD\n')
            for i,m in enumerate(missing):
                f.write(str(i+1)+'\t'+m+'\n')
    ff.write('{0}\t{1}\t{2}\t{3:.2f}\n'.format(
        t,
        c,
        len(missing),
        100 * c/len(concepts)))
ff.close()
