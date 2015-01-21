from lingpyd import *
import re
# first get allens list as good as possible
allen = csv2list('Allen-2007-500.tsv')
allend= dict([(b,(a,c,d)) for a,b,c,d in allen if d != 'NAN'])

loc = csv2list('loc.tsv')
locd = dict([(x[1], x[0]) for x in loc])
locowid = [x[1] for x in loc]

newads = csv2list('matches.tsv')
newadd = dict([(b,c) for a,b,c,d in newads])

wl = Wordlist('bai.tsv')

owid = {}
owids = []
missing = []
for k in wl:
    src = wl[k,'source']
    gls = wl[k,'gloss_in_source']
    concept = wl[k,'concept']
    if gls in allend:
        owid[concept] = allend[gls][-1]
        owids += [allend[gls][-1]]
    elif concept in newadd:
        owid[concept] = newadd[concept]


    
#missing = [x for x in locd if x not in owids]
#with open('missing.tsv', 'w') as f:
#    for m in missing:
#        f.write('{0}\t{1}\n'.format(m,locd[m]))


## search for potentially good entries
#matches = []
#still_missing = []
#for m in missing:
#    rawm = locd[m]
#    strips = ['to ', 'the ']
#    for s in strips:
#        rawm = rawm.replace(s,'')
#    rawm = re.sub(r' \(.*?\)','',rawm)
#    rawm = re.sub(r' \[.*?\]','',rawm)
#    
#    if rawm in wl.concepts:
#        print('Possible match for {0} with {1}'.format(rawm,rawm))
#        matches += [(m,locd[m],rawm)]
#    else:
#        still_missing += [(m,locd[m],'?')]
#
#with open('missing.tsv', 'w') as f:
#    for i,(a,b,c) in enumerate(still_missing+matches):
#        print(a,b,c)
#        f.write(str(i+1)+'\t'+'\t'.join([c,a,b])+'\n')
#

wl.add_entries('omegawiki', 'concept', lambda x: owid[x] if x in owid else '?')
wl.add_entries('source', 'source,id_in_source', 
        lambda x,y: x[y[0]] +', '+x[y[1]], override=True)
wl.add_entries('gloss_in_source', 'gloss_in_source,chinese_gloss',
        lambda x,y: x[y[0]] +' / '+ x[y[1]] if x[y[1]] != '?' else x[y[0]], override=True)
wl.output('tsv', filename='bai_subset', subset=True,
        cols = [
            'ipa',
            'source',
            'gloss_in_source',
            'entry_in_source',
            'pos',
            'doculect',
            'concept',
            'omegawiki',
            'chinese_gloss'],
        rows = dict(
            omegawiki = 'in '+str(sorted(locd)))
            )
#lex = LexStat('bai_coverage.tsv', check=True, merge_vowels=False)
##lex.cluster(method='edit-dist', threshold=0.5)
#D = lex.get_distances(method='sca')
#lex._meta['distances'] = D
#lex.calculate('tree',)
#lex.calculate('groups', threshold=0.2)
#lex.output('groups')
#from lingpyd.convert.plot import plot_tree
#
## get specific labels according to sources
#ts = {}
#for k in lex:
#    t = lex[k,'taxon']
#    s = lex[k,'source']
#    if s == 'Allen2007':
#        sr = 'A'
#    else:
#        sr = 'W'
#    if t not in ts:
#        ts[t] = t+'_'+sr
#
#
#
#plot_tree(lex.tree, labels=ts)
#lex.output('tsv', filename='bai_coverage_lingpy',
#        ignore=['msa','json','dst','scorer','distances'])
