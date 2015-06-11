# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-08 10:26
# modified : 2015-04-08 10:26
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-04-08"

from lingpyd import *
from lingpyd.basic.ops import clean_taxnames
from lingpyd.meaning.glosses import parse_gloss, compare_conceptlists, compare_concepts
from lingpyd.plugins.lpserver import lexibase as lb

from sys import argv


if 'tbl' in argv and 'compile' in argv:
    # preformat wordlists
    wl = Wordlist('data/TBL.csv', col='language', row='gloss')
    
    # get part of speech information 
    pos = {}

    # check for consistent identifiers
    D = {}
    for k in wl:
        
        c = wl[k,'concept']
        s = wl[k,'srcid'].split('.')[0]
        
        if s:
            if s not in pos:
                if wl[k,'gfn'] in ['n', 'n.', 'Nanim', 'nbp', 'nrel', 'nveg']:
                    p = ' (noun)'
                elif wl[k,'gfn'] in ['v', 'v.', 'be v.']:
                    p = ' (verb)'
                elif wl[k,'gfn'] in ['vi', 'vi.']:
                    p = ' (verb, intransitive)'
                elif wl[k,'gvn'] in ['vt']:
                    p = ' (verb, transitive)'
                else:
                    p = ''

                pos[s] = p #wl[k,'gfn']
    
        try:
            D[s] += [c]
        except:
            D[s] = [c]
    
    pos[''] = ''

    count = 1
    C = {}
    for k in D:
        C[k] = sorted(D[k], key=lambda x: D[k].count(x), reverse=True)[0]
    
    wl.add_entries('stedt_gloss', 'gloss', lambda x: x)
    wl.add_entries('concept', 'srcid', 
            lambda x: C[x.split('.')[0]]+pos[x.split('.')[0]]
                )
    
    wl.output('tsv', filename='data/tbl', subset=True, cols=[x for x in
        wl.header if x != 'gloss'])
    
    # make conceptlist for TBL
    wl = Wordlist('data/tbl.tsv')
    L = []
    for k in wl:
        c = wl[k,'concept']
        s = wl[k,'srcid'].split('.')[0]
        L += [(s,c)]
    
    with open('tbl_concepts.tsv', 'w') as f:
        f.write('NUMBER\tGLOSS\n')
        for a,b in sorted(set(L)):
            if a:
                f.write(a+'\t'+b+'\n')

if 'zmyyc' in argv and 'compile' in argv:

    wl = Wordlist('data/ZMYYC.csv', col='language', row='gloss')
    
    # get part of speech information 
    pos = {}

    # check for consistent identifiers
    D = {}
    for k in wl:
        
        c = wl[k,'concept']
        s = wl[k,'srcid'].split('.')[0]
        
        if s:
            if s not in pos:
                if wl[k,'gfn'] in 'xxx' and wl[k,'gfn']: #['n', 'n.', 'Nanim', 'nbp', 'nrel', 'nveg']:
                    p = ' (noun)'
                elif wl[k,'gfn'] in ['v', 'v.', 'be v.']:
                    p = ' (verb)'
                elif wl[k,'gfn'] in ['vi', 'vi.']:
                    p = ' (verb, intransitive)'
                elif wl[k,'gvn'] in ['vt']:
                    p = ' (verb, transitive)'
                else:
                    p = ''

                pos[s] = p #wl[k,'gfn']
    
        try:
            D[s] += [c]
        except:
            D[s] = [c]
    
    pos[''] = ''

    count = 1
    C = {}
    for k in D:
        C[k] = sorted(D[k], key=lambda x: D[k].count(x), reverse=True)[0]
    
    wl.add_entries('stedt_gloss', 'gloss', lambda x: x)
    wl.add_entries('concept', 'srcid', 
            lambda x: C[x.split('.')[0]]+pos[x.split('.')[0]]
                )
    
    wl.output('tsv', filename='data/zmyyc', subset=True, cols=[x for x in
        wl.header if x != 'gloss'])
    
    # make conceptlist for TBL
    wl = Wordlist('data/zmyyc.tsv')
    L = []
    for k in wl:
        c = wl[k,'concept']
        s = wl[k,'srcid'].split('.')[0]
        L += [(s,c)]
    
    with open('zmyyc_concepts.tsv', 'w') as f:
        f.write('NUMBER\tGLOSS\n')
        for a,b in sorted(set(L),key=lambda x: int(x[0])):
            if a:
                f.write(a+'\t'+b+'\n')


if 'stdb' in argv and 'compile' in argv:
    db = lb.LexiBase('sinotibetan', dbase='sinotibetan.sqlite3',
        #url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3', 
        )
    
    L = []
    b = []
    g = []
    for k in db:
    
        c = db[k,'concept']
        s = db[k,'omegawiki']
    
        if s:
            L += [(s,c)]
            g += [c]
        else:
            b += [c]
    with open('stdb_concepts.tsv', 'w') as f:
        f.write('NUMBER\tGLOSS\n')
        for a,b in sorted(set(L), key=lambda x: (x[1].lower(),x[0])):
            f.write(a + '\t'+b+'\n')



if 'compare' in argv:

    clists = compare_conceptlists(
            #'stdb_concepts.tsv',
            argv[1]+'_concepts.tsv',
            argv[2]+'_concepts.tsv',
            output = 'tsv', 
            filename=argv[1]+'_vs_'+argv[2],
            match = [1,2,3,4,5,6,7],
            debug = True
            )
    


