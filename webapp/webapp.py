# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-06 14:55
# modified : 2015-05-06 14:55
"""
Create a web-app with additional information and quick access to the database.
"""

__author__="Johann-Mattis List"
__date__="2015-05-06"


#import os
#os.system('mv sinotibetan.sqlite3 ~/projects/websites/dighl/triples/')
from lingpy import *
from lingpy._plugins.lpserver.lexibase import LexiBase,load_sqlite
import json
from pystdb import *

# in later steps:
# re-link the data
db = load_sinotibetan()

print("loaded the db")
# we expand on the meta-data template
with open('../metadata/metadata.json') as f:
    meta = json.loads(f.read())

mcon = stdb_concepts()


txt1 = ''
concepts = sorted(set([db[k,'concept'] for k in db]))
preselected_taxa="""Bai_Jianchuan|Bokar|Daofu|Darang_Taraon|Dulong|Japhug|Jingpho|Khaling|Limbu|Lisu|Motuo_Menba|Naxi|Old_Burmese|Old_Chinese|Pumi_Lanping|Qiang_Mawo|rGyalrong_Maerkang|Tibetan_Written|Tujia|Yidu|Xumi|Lyuzu|Zhaba_Daofu_County""".split('|')
visited = []
for c in concepts:
    visited += [c]
    # determine coverage
    cov = len([db[k,'concept'] for k in db if db[k,'concept'] == c])
    print('Analysed concept {0}'.format(c))
    if c in mcon:
        txt1 += '<option value="'+c+'" selected>'+c+' ('+str(cov)+' entries)</option>'
    else:
        txt1 += '<option value="'+c+'">'+c+' ('+str(cov)+' entries)</option>'

print([c for c in concepts if c not in visited])


txt2 = ''

langs = db.taxa 
conv = dict([(k,v['subgroup']) for k,v in meta.items()])

print('computed coverage')

for k in langs:
    etr = len(db.get_list(doculect=k,flat=True))
    if k in preselected_taxa:
        txt2 += '<option value="'+k+'" selected>'+k+' ('+conv[k]+', '+str(etr)+' entries)</option>'
    else:
        txt2 += '<option value="'+k+'">'+k+' ('+conv[k]+', '+str(etr)+' entries)</option>'

txt3 = ''

header = ['doculect', 'borrowing', 'chinese', 'cogid', 'concept', 'ipa',
        'tokens', 'note', 'hanzi']
for col in sorted(db.header, key=lambda x: db.header[x]):
    if col in header:
        txt3 += '<option value="'+col.upper()+'" selected>'+col.upper()+'</option>'
    else:
        txt3 += '<option value="'+col.upper()+'">'+col.upper()+'</option>'


# we expand on the meta-data template
with open(stdb_path('metadata', 'metadata.json')) as f:
    meta = 'META = '+json.dumps(json.loads(f.read()))+';'

with open(stdb_path('webapp', 'templates', 'index.template.html')) as f:
    d = f.read()
    d = d.format(JS=open('templates/stb.js').read(), 
            DOCULECTS = txt2,
            CONCEPTS  = txt1,
            CONTENT = txt3,
            META = meta
            )
with open('index.html', 'w') as f:
    f.write(d)        
