from lingpy import *
from pystdb import *
import os

cnc = load_concepticon()
wl = load_stedt('KVB-PKC.csv')
falam = wl.get_list(col='Lai (Hakha)', flat=True)
with open('VanBik-2009-724.tsv', 'w') as f:
    f.write('{0}\t{1}\n'.format('ID', 'ENGLISH'))
    for k in falam:
        concept = wl[k, 'concept']
        idx = wl[k, 'rn']
        if concept.strip():
            f.write(idx+'\t'+concept+'\n')
os.system('concepticon map_concepts VanBik-2009-724.tsv vbk.mapped.out')
csv = csv2list('vbk.mapped.out')
concepts = stdb_concepts()
cids = [c['concepticon_id'] for c in concepts.values()]
vkg = []
for line in csv:
    if len(line) > 2:
        vkg += [line[2]]
common = [c for c in cids if c in vkg]
for k in [x for x in concepts if concepts[x]['concepticon_id'] not in vkg]:
    print(k)
