# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-27 13:03
# modified : 2015-04-27 13:03
"""
import new data (TBL)
"""

__author__="Johann-Mattis List"
__date__="2015-04-27"

from lingpy import *
from lingpyd.plugins.lpserver.lexibase import LexiBase,load_sqlite

changes = dict([
        ('the breast','the breast (female)'),
        ('the hair', 'the hair (of the head)'), 
        ('to plant','to plant (vegetals, rice)'),
        ('we [first person plural]', 'we [first person plural inclusive]'),
        ])

base = csv2list('matches.tsv')

_groups = csv2list('tbl.languages.tsv')
groups = {}
for g in _groups:
    groups[g[1].strip()] = g[3].split(' - ')[1]

clean = lambda x: ''.join([y for y in x if y not in '[]()?{}']).replace(' ','_')

wl = LexiBase(load_sqlite('sinotibetan', 'sinotibetan.sqlite3',
    url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3'
    ))
for k in wl:
    concept = wl[k,'concept']
    if concept in changes:
        wl[k][wl.header['concept']] = changes[concept]
wl.add_entries('taxon_name_in_source','doculect',lambda x: x)

wl2 = Wordlist('tbl-stdb.tsv')
wl2.add_entries('source','ipa',lambda x: 'STEDT/TBL')
wl2.add_entries('STEDT_TAXON_NAME', 'doculect', lambda x:x)

for k in wl2:
    wl2[k][wl2.header['doculect']] = clean(wl2[k,'taxa'])
wl2.add_entries('subgroup', 'stedt_taxon_name', lambda x: groups[x])

wl2.output('tsv', filename='tbl-update', subset=True, rows=dict(
    subgroup = '!= "Burmish"', ipa = '!= "*"'))
wl2 = Wordlist('tbl-update.tsv')


blacklist = []
for k in wl.taxa:
    entries = wl.get_list(doculect=k, entry='ipa', flat=True)
    if len(set(entries)) < 10:
        blacklist += wl.get_list(doculect=k, flat=True)


commons = [t for t in wl.taxa if t in wl2.taxa]
for k in wl:
    if wl[k,'taxa'] in commons or wl[k,'subgroup'] == 'Burmish':
        blacklist += [k]

wl.blacklist = blacklist
wl.add_data(wl2)


check = lambda x: ''.join([y for y in x if y not in '*?!- ']).strip()
D = {}
D[0] = sorted(wl.header, key=lambda x: wl.header[x])
for k in wl:
    if k not in blacklist and check(wl[k,'ipa']):
        D[k] = wl[k]
wln = LexiBase(D)
wln.create('sinotibetan', dbase='sinotibetan.sqlite3')

#wl.output('tsv', filename='sinotibetan-dbase', subset=True, rows=dict(
#    ID = 'not in '+str(blacklist)))
#wl.create('sinotibetan', dbase='sinotibetan.sqlite3', ignore=False)

#import os
#os.system('mv sinotibetan.sqlite3 ~/projects/websites/dighl/triples/')
#
#
## in later steps:
## re-link the data
#db = LexiBase('sinotibetan.sqlite3')
#txt1 = ''
#concepts = sorted(set([db[k,'concept'] for k in db]))
#for c in concepts:
#    
#    # determine coverage
#    cov = len([db[k,'concept'] for k in db if db[k,'concept'] == c])
#    if cov > 7:
#        txt1 += '<option value="'+c+'" selected>'+c+' ('+str(cov)+')</option>'
#    else:
#        txt1 += '<option value="'+c+'">'+c+'('+str(cov)+')</option>'
#
#txt2 = ''
#langs = [db[k,'taxon'] for k in db]
#langs = sorted(set(langs))
#
#for k in langs:
#    txt2 += '<option value="'+k+'">'+k+'</option>'
#
#txt3 = ''
#for col in sorted(db.header, key=lambda x: db.header[x]):
#    txt3 += '<option value="'+col.upper()+'" selected>'+col.upper()+'</option>'
#
#with open('website/index.template.html') as f:
#    d = f.read()
#    d = d.format(JS=open('website/stb.js').read(), 
#            DOCULECTS = txt2,
#            CONCEPTS  = txt1,
#            CONTENT = txt3
#            )
#with open('website/index.html', 'w') as f:
#    f.write(d)        
