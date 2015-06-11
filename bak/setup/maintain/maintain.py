# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-01 11:32
# modified : 2015-04-01 11:32
"""
Basic maintenance script, accepts csv-statements, downloads the data, and
changes the entries.
"""

__author__="Johann-Mattis List"
__date__="2015-04-01"

import lingpyd as lingpy
from util import get_sinotibetan
from sys import argv

# settings for each session, defaults already predefined
settings = dict(
        remote = True,
        )

# overwrites array stores those things which are not multiply definable
overwrites = ['remote', 'removeEmptyRows']

for arg in argv:
    if '=' in arg:
        a,b = arg.split('=')

        if b in ['True','False']:
            b = eval(b)
        
        if a in settings and a not in overwrites:
            if isinstance(settings[a], list):
                settings[a] += [b]
            else:
                settings[a] = [settings[a],b]
        elif a in settings and a in overwrites:
            settings[a] = b
        else:
            settings[a] = b
    else:
        settings[arg] = True

if 'debug' in settings:
    print(settings)

db = get_sinotibetan(remote=settings['remote'])

# check for bad id columns
for k in db:
    for idx in ['scaid', 'cogid']:
        cogid = db[k,idx]
        if not isinstance(cogid, int) and not str(cogid).isdigit():
            print("Re-adjusted cognate ID, replace «{0}» with {1} (ID:{2})".format(
                db[k,idx], 0, k))
            db[k][db.header[idx]] = 0

if 'addDoculect' in settings:
    
    if isinstance(settings['addDoculect'], list):
        docs = settings['addDoculect']
    else:
        docs = [settings['addDoculect']]
    for doculect in docs:
        db.add_doculect(doc, ['omegawiki'])

if 'modifyValue' in settings:
    
    if isinstance(settings['modifyValue'], list):
        mods = settings['modifyValue']
    else:
        mods = [settings['modifyValue']]
    for mod in mods:
        print(mod)
        s,t,c = mod.split('//')
        db.modify_value(s,t,c)

if 'removeEmptyRows' in settings:

    if settings['removeEmptyRows'] == True:
        for doculect in db.doculect:
            db.remove_empty_rows(doculect)
    else:
        if not ':' in settings['removeEmptyRows']:
            doculects = settings['removeEmptyRows']
            for doculect in doculects.split('//'):
                db.remove_empty_rows(doculet)
        else:
            doculects,entries = settings['removeEmptyRows'].split(':')
            entries = entries.split('//')
            for doculect in doculects.split('//'):
                db.remove_empty_rows(doculect, entries=entries)

if 'removeValue' in settings:
    
    if isinstance(settings['removeValue'], list):
        rems = settings['removeValue']
    else:
        rems = [settings['removeValue']]
    for rem in rems:
        print(rem)
        s,t = rem.split('//')
        db.remove_values(s,t)

if 'addWordlist' in settings:
    
    if isinstance(settings['addWordlist'], list):
        wls = settings['addWordlist']
    else:
        wls = [settings['addWordlist']]
    for f in wls:
        wl = lingpy.Wordlist(f)
        db.add_data(wl)

db.update('sinotibetan')
db.create('sinotibetan')

import os 
os.system('mv *blacklist.log blacklists/')

db._clean_cache()
db.output('tsv', filename='.tmp', subset=True, rows=dict(
    ID = 'not in '+str(db.blacklist)))
db = lingpy.Wordlist('.tmp.tsv')

# count average number of entries per taxon
entries = []
for t in db.doculect:
    tmp = db.get_dict(taxon=t)
    
    count = 0
    for k in tmp:
        if tmp[k]:
            if ''.join([x for x in str(db[tmp[k][0],'ipa']) if x not in '- ?']):
                count += 1
    entries += [count]
coverage = dict(zip(db.taxa,entries))
w,h = db.width, db.height

# create template
taxa = sorted(set([db[k,'doculect'] for k in db]))
groups = {}
for k in db:
    t = db[k,'doculect']
    g = db[k,'subgroup']

    if g:
        groups[t] = g
for t in taxa:
    if t not in groups:
        groups[t] = '?'
concepts = sorted(set([db[k,'concept'] for k in db]))
columns = sorted(db.header, key=lambda x: db.header[x])

tstr = ''
for t in taxa:
    tstr += '<option value="{0}">{0} ({1}, {2} concepts)</option>\n'.format(
            t, groups[t], coverage[t])
cstr = ''
for concept in concepts:
    cstr += '<option value="{0}" selected>{0}</option>\n'.format(concept)

colstr = ''
goodies = ['doculect', 'concept', 'entry_in_source', 'ipa', 'tokens', 'hanzi',
        'gloss_in_source', 'note', 'wold']
for col in sorted(db.header):
    
    if col in goodies:
        sel = ' selected'
    else:
        sel = ''
    colstr += '<option value="{0}"{1}>{2}</option>'.format(
            col.upper(),
            sel,
            col.upper().replace('_',' '))


with open('index.html', 'w') as f:

    tmpl = open('templates/template.html').read()
    js = open('templates/stb.js').read()

    txt = tmpl.format(
            taxa = tstr,
            concepts = cstr,
            columns = colstr,
            width = w,
            height = h,
            javascript = js,
            coverage = sum(sorted(coverage.values())) / len(coverage)
            )
    f.write(txt)
