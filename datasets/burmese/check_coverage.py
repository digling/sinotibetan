# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-10 14:27
# modified : 2015-03-10 14:27
"""
Check concept coverage for burmish data (from STEDT)
"""

__author__="Johann-Mattis List"
__date__="2015-03-10"


from lingpyd import *
from lingpyd.plugins.chinese.sinopy import clean_chinese_ipa
from lingpyd.plugins.lpserver.lexibase import LexiBase

# load stb data (today's status)
db = LexiBase('sinotibetan', dbase='../../sqlite/sinotibetan.sqlite3',
        #url='http://tsv.lingpy.org/triples/triples.sqlite3'
        )

bm = csv2list('burmese.tsv')


concepts = {}
for k in db:

    owid = db[k,'omegawiki']
    conc = db[k,'concept']
    
    try:
        concepts[owid] += [conc]
    except:
        concepts[owid] = [conc]

burmese = {}
for k in bm[1:]:

    try:
        burmese[k[4]] += [k[1]]
    except:
        burmese[k[4]] = [k[1]]

count = 0
for k in concepts:
    if k in burmese:
        count += 1
    else:
        print('//'.join(sorted(set(concepts[k]))))

print(count, len(concepts), count / len(concepts))

with open('bst.tsv', 'w') as f:

    for k in burmese:

        if k in concepts:
            f.write('\n'.join(burmese[k])+'\n')
        else:
            pass

