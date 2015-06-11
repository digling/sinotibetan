# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-01-20 10:18
# modified : 2015-01-20 10:18
"""
This script creates the initial version of the database. 

Further scripts will be written in order to guarantee that the database can be
edited with help of Python/LingPy automatically.
"""

__author__="Johann-Mattis List"
__date__="2015-01-20"


from lingpyd.plugins.lpserver.lexibase import * 
import lingpyd as lingpy
from sys import argv

make_lexibase('lot.tsv', 'loc.tsv', 
        ['ENTRY_IN_SOURCE','IPA','TOKENS','ALIGNMENT','NOTE',
        'GLOSS_IN_SOURCE', 'HANZI', 'COGID', 'SOURCE','SCAID'],
        filename='sino-tibetan')


db = LexiBase('sino-tibetan.tsv')
db.dbase = 'dbase/sinotibetan.sqlite3'
from glob import glob
taxa = glob('taxa/*.tsv')

def clean_ipa(ipa):

    ipa = ipa.replace('-', lingpy.rc('morpheme_separator'))
    ipa = ipa.replace(' ', '_')

    ipa = ipa.replace('(','')
    ipa = ipa.replace('(','')
    ipa = ipa.replace('*','')
    ipa = ipa.replace('[','')
    ipa = ipa.replace(']','')

    ipa = ipa.replace('h', 'ʰ')

    return ipa

modified = []
for t in taxa:
    name = t.split('/')[1].split('.')[0]
    if name in db.taxa:
        dt = lingpy.csv2list(t)
        dd = dict([(a,b) for a,*b in dt[1:]])
        hd = dt[0][1:]
        entries = db.get_list(taxon=name)
        owids = [db[idx,'omegawiki'] for idx in entries]
        for e,o in zip(entries, owids):
            if o in dd:
                modified += [e]
                for i,h in enumerate(hd):
                    tag = h.lower()
                    if tag != 'omegawiki' and tag != 'ipa' and dd[o]:
                        if tag == 'alignment':
                            print(tag,dd[o][i])
                        db[e][db.header[tag]] = dd[o][i]
                    elif tag == 'ipa' and 'tokens' not in hd:
                        ipa = dd[o][i]
                        #ipax = ipa.replace('-', rc('morpheme_separator'))
                        #ipax = ipa.replace(' ', '_')
                        tks = clean_ipa(ipa)
                        try:
                            tks = lingpy.ipa2tokens(tks, expand_nasals=True,
                                    semi_diacritics='hsɕʑʐʂ',
                                    merge_vowels=False)
                        except:
                            tks = list(ipa)
                        db[e][db.header['ipa']] = ipa
                        db[e][db.header['tokens']] = tks
                        db[e][db.header['entry_in_source']] = ipa
                    else:
                        print(tag)
                        db[e][db.header[tag]] = dd[o][i]


db.add_entries('cogid_', 'concept,cogid', lambda x,y:
        str(x[y[0]])+':'+str(x[y[1]]))
db.renumber('cogid_', 'cogid', override=True)
db.add_entries('borrowing', 'ipa', lambda x: '1' if x.startswith('%') else '');

for k in db:
    if k in modified:
        pass
    else:
        db[k][db.header['cogid']] = 0
    #db[k][db.header['alignment']] = ''
        

for k in db:
    for h,i in db.header.items():
        if db[k][i] == '-':
            db[k][i] == ''
    if db[k,'ipa'].startswith('%'):
        ipa = db[k,'ipa'][1:]
        tks = [t for t in db[k,'tokens'][1:]]
        print('foundit',db[k,'ipa'])
        db[k][db.header['ipa']] = ipa #db[k,'ipa'][1:]
        db[k][db.header['tokens']] = tks #db[k,'tokens'][1:]
db._clean_cache()


# add data from Laurent
#ls = lingpy.csv2list('OCLS.tsv')
# get all data for ABVD
#abvd = {}
#for k in db:
#    if db[k,'taxon'] == 'Old_Chinese':
#        
#        abvdx = db[k,'abvd']
#        
#        if abvdx != '-':
#
#            abvdx = abvdx[abvdx.index('(')+1:-1]
#            for x in abvdx.split(' // '):
#                abvd[abvdx] = k
#for line in ls[1:]:
#    cidx = line[0]
#    
#    if cidx in abvd:
#        print('found '+line[1]+' for OCH')
#        widx = abvd[cidx]
#        orig = line[1]
#        char = line[3]
#        db[widx][db.header['ipa']] = line[2]
#        try:
#            tks = lingpy.ipa2tokens(clean_ipa(line[2]))
#        except:
#            tks = list(clean_ipa(line[2]))
#        if line[3]:
#            db[widx][db.header['hanzi']] = line[3]
#        db[widx][db.header['tokens']] = tks
#        db[widx][db.header['gloss_in_source']] = line[1]
#        db[widx][db.header['entry_in_source']] = line[2]
#
#db.output('tsv', filename='taxa/Old_ChineseLS.tsv', subset=True, 
#        cols=['omegawiki', 'gloss_in_source', 'ipa', 'cogid', 'hanzi'],
#        rows=dict(taxa='== "Old_Chinese"'))

if 'update' in argv:
    db.output('tsv', filename='sinotibetan', subset=True, cols=[c for c in
        db.header if c[-1] != '_'], ignore=['json'])
    db = LexiBase('sinotibetan.tsv')
    
    db.update('sinotibetan',ignore=['cogid_'],dbase='../sqlite/sinotibetan.sqlite3')

# XXX
# basically works, settle issue with cognate ids (leave untouched)
# settle also issue with tokens and alignments, add tokens for the moment
# add bai-data 
# solve borrowing-issue by adding a "borrowed" tag and something more DONE

# create the html file for selecting the values
txt = ''
for t in db.taxa:
    subs = db.get_list(taxon=t,entry='subgroup', flat=True)[0]
    txt += '<option value="{0}">{1} ({2})</option>\n'.format(t,t.replace('_',' '),subs)
taxa = '  <select class="selex" id="doculects" multiple>\n'+txt+'</select>\n'
txt = ''
for c in db.concepts:
    txt += '  <option value="{0}" selected>{1}</option>\n'.format(c,c)
concepts = '<select class="selex" id="concepts" multiple>\n'+txt+'</select>\n'
txt = ''
for h in sorted(db.header):
    if h in ['ipa', 'doculect', 'concept', 'tokens', 'cogid', 'note',
    'entry_in_source', 'gloss_in_source','wold','omegawiki']:

        txt += '  <option value="{0}" selected>{1}</option>\n'.format(h.upper(),h)
    else:
        txt += '  <option value="{0}">{1}</option>\n'.format(h.upper(),h)
columns = '<select class="selex" id="columns" multiple>\n'+txt + '</select>\n'
tmp = open('sinotibetan/template.html').read()
javascript = open('sinotibetan/stb.js').read()
with open('sinotibetan/index.html', 'w') as f:
    f.write(tmp.format(taxa=taxa,concepts=concepts,columns=columns,javascript=javascript))
