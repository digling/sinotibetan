# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-27 12:25
# modified : 2015-04-27 12:25
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-04-27"

from lingpyd import *
from lingpyd.sequence.sound_classes import syllabify

concepts = csv2list('matches.tsv')
keys = [x[-1] for x in concepts[1:]]
oris = dict([(x[-1],x[1]) for x in concepts[1:]])
wl = Wordlist('tbl.tsv')
keep = []
D = {}
D[0] = sorted(wl.header, key=lambda x: wl.header[x]) + ['STEDT_RN']
for k in wl:
    srcid = wl[k,'srcid'].split('.')
    if len(srcid) > 1:
        cid = srcid[0]
        if cid in keys:
            keep += [k]
            D[k] = wl[k]
            D[k][wl.header['concept']] = oris[cid]
            D[k] += [str(k)]



print('compared stuff')
wln = Wordlist(D)

def fun(x):
    try:
        return ' _ '.join([' '.join(syllabify(ipa2tokens(y, merge_vowels=False, expand_nasals=True,
    semi_diacritics='shzʃʑʒɕʐʂθ'))) for y in x.split(' ')]).split(' ')
    except:
        return ['???'] + list(x)

wln.add_entries('ipa', 'reflex', lambda x: x)
wln.add_entries('tokens', 'reflex', lambda x: fun(x))

    #ipa2tokens(x.replace(' ','_'), merge_vowels=False, expand_nasals=True,
    #    semi_diacritics='shzʃʑʒɕʐʂθ')))
for k in wln:
    wln[k][wln.header['tokens']] = ' '.join(wln[k,'tokens']).replace('_ ◦','_').split(' ')
wln.output('tsv', filename='tbl-stdb')

