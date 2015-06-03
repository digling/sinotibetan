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

# get concepts
new_concepts = [w[1] for w in csv2list('stdb.concepts.csv') if w[3] == 'NEW']
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
            count = 1
            for i,m in enumerate(missing):
                if m in new_concepts:
                    f.write(str(count)+'\t'+m+'\n')
                    count += 1
    ff.write('{0}\t{1}\t{2}\t{3:.2f}\n'.format(
        t,
        c,
        len(missing),
        100 * c/len(concepts)))
ff.close()

db.output('tsv', filename='stdb-2015-05-06')

