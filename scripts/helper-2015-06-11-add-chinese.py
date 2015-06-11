# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-11 12:41
# modified : 2015-06-11 12:41
"""
add chinese dialect data to the sinotibetan database
"""

__author__="Johann-Mattis List"
__date__="2015-06-11"

from lingpyd.plugins.lpserver.lexibase import LexiBase
from lingpyd import *

db = LexiBase('sinotibetan', dbase='../sqlite/sinotibetan.sqlite3', 
        url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3'
        )

wl = Wordlist('../datasets/BeijingDaxue/beida-subset-aligned.tsv')
subgroups = dict([(line[1],line[3]) for line in
    csv2list('../datasets/BeijingDaxue/beida.taxa', header=True)])

# add subgroups to data
wl.add_entries('subgroup', 'doculect', lambda x: 'Sinitic')

# modify cognate ids
ignore = [
    'borrowed',
    'abvd',
    'ielex',
    'swadesh_1952',
    'swadesh_1955',
    'tower_of_babel',
    'wold',
    'scaid',
    '_cogid',
    ]

for k in wl:
    cogid = wl[k,'cogid']
    cogid += 10000
    wl[k][wl.header['cogid']] = cogid

db.add_data(wl)
db.add_entries('_cogid', 'cogid', lambda x: x if isinstance(x, int) else 0)
db.renumber('_cogid', 'cogid')
db.create('sinotibetan', ignore=ignore)

import os
os.system('cp sinotibetan.sqlite3 ~/projects/scripts/edictor/triples/')

