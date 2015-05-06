#import os
#os.system('mv sinotibetan.sqlite3 ~/projects/websites/dighl/triples/')
from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase,load_sqlite

# in later steps:
# re-link the data
db = LexiBase('sinotibetan', dbase='sinotibetan.sqlite3')

mcon = [w[1] for w in csv2list('matches.tsv')]
txt1 = ''
concepts = sorted(set([db[k,'concept'] for k in db]))
for c in concepts:
    
    # determine coverage
    cov = len([db[k,'concept'] for k in db if db[k,'concept'] == c])
    if c in mcon:
        txt1 += '<option value="'+c+'" selected>'+c+' ('+str(cov)+' entries)</option>'
    else:
        txt1 += '<option value="'+c+'">'+c+' ('+str(cov)+' entries)</option>'

txt2 = ''
langs = [(db[k,'taxon'],db[k,'subgroup']) for k in db]

langs = sorted(set(langs))
conv = dict(langs)
langs = sorted(set([x[0] for x in langs]))

for k in langs:
    etr = len(db.get_list(doculect=k,flat=True))
    txt2 += '<option value="'+k+'">'+k+' ('+conv[k]+', '+str(etr)+' entries)</option>'

txt3 = ''
for col in sorted(db.header, key=lambda x: db.header[x]):
    txt3 += '<option value="'+col.upper()+'" selected>'+col.upper()+'</option>'

with open('website/index.template.html') as f:
    d = f.read()
    d = d.format(JS=open('website/stb.js').read(), 
            DOCULECTS = txt2,
            CONCEPTS  = txt1,
            CONTENT = txt3
            )
with open('website/index.html', 'w') as f:
    f.write(d)        
