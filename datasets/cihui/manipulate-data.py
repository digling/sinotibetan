from pystdb import stdb_concepts
from lingpy import *

concepts = stdb_concepts()
wl = Wordlist('cihui-edited-2017-08-08.tsv')

D = {}
idx = max(wl)+1


D[0] = sorted(wl.header, key=lambda x: wl.header[x])
for k in wl:
    D[k] = wl[k]


# select which concepts to add
for taxon in wl.cols:
    data = wl.get_list(col=taxon, flat=True, entry='concept')
    for concept in concepts:
        if concept not in data:
            D[idx] = ['' for k in D[0]]
            D[idx][wl.header['doculect']] = taxon
            D[idx][wl.header['concept']] = concept
            D[idx][wl.header['cogids']] = '0'
            idx += 1
for concept in concepts:
    D[idx] = ['' for k in D[0]]
    D[idx][wl.header['doculect']] = 'Chaozhou'
    D[idx][wl.header['concept']] = concept
    D[idx][wl.header['cogids']] = '0'
    idx += 1
wl = Wordlist(D)
wl.add_entries('rank', 'concept', lambda x: concepts.get(x, {"rank": '0'})['rank'])
wl.output('tsv', filename='chinese-template', prettify=False, ignore='all')
