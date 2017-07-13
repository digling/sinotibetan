from lingpy import *
from pystdb import *
import os

cnc = load_concepticon()
wl = load_stedt('GEM-CNL.csv')
falam = wl.get_list(col='Lushai [Mizo]', flat=True)
with open('tmp.tsv', 'w') as f:
    f.write('{0}\t{1}\n'.format('ID', 'ENGLISH'))
    for k in falam:
        concept = wl[k, 'concept']
        idx = wl[k, 'rn']
        if concept.strip():
            f.write(idx+'\t'+concept+'\n')
os.system('concepticon map_concepts tmp.tsv tmp.mapped.tsv')
csv = csv2list('tmp.mapped.tsv')
concepts = stdb_concepts()
cids = [c['concepticon_id'] for c in concepts.values()]
vkg = []
for line in csv:
    if len(line) > 2:
        vkg += [line[2]]
common = [c for c in cids if c in vkg]
for k in [x for x in concepts if concepts[x]['concepticon_id'] not in vkg]:
    print(k)
print(len(common), '{0:.2f}'.format(len(common) / len(concepts)))
