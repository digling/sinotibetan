from lingpy import *
from pystdb import *
from collections import defaultdict

stb = load_sinotibetan(remote=True)
source = 'Burling2003'

wl = Wordlist('RB-LMMG.csv', row='gloss', col='language')
mapped = csv2list('rbm.csv', strip_lines=False)

D = {}
for i, line in enumerate(mapped[1:]):
    print(line)
    if line[3].strip() == '!':
        pass
    else:
        concept, idx = line[1], int(line[2])
        gis = wl[idx, 'gloss']
        lng = 'Garo'
        wrd = wl[idx, 'reflex']
        tks = ' + '.join([' '.join(ipa2tokens(c.replace(' ',
            '_').replace('•','+'),
            semi_diacritics='h', merge_vowels=False)) for c in wl[idx, 'reflex'].split('.')])
        iis = wl[idx, 'rn']
        D[i+1] = [concept, gis, wrd, tks, iis, lng, source, 0]
D[0] = ['concept', 'gloss_in_source', 'ipa', 'tokens', 'rgen', 'doculect',
        'source', 'cogid']
wl = Wordlist(D)
stb.add_data(wl)
stb.update('sinotibetan')

