from lingpy import *
from pystdb import *

c1 = csv2list(stdb_path('concepts', 'concepts.tsv'))
c2 = csv2list(stdb_path('concepts', 'concepts-2017-07-13.tsv'))

c1d = {v[1]: dict(zip([h.lower() for h in c1[0]], v)) for v in c1[1:]}
c2d = {v[1]: dict(zip([h.lower() for h in c2[0]], v)) for v in c2[1:]}

header = [h.lower() for h in c1[0]]
out = [[h.upper() for h in header]+['RANK']]
for k, vals in c1d.items():
    row = [vals[h] for h in header]
    row += [c2d[k]['rank']]
    out += [row]
with open(stdb_path('concepts', 'conceptsx.tsv'), 'w') as f:
    f.write('\t'.join(out[0])+'\n')
    for line in sorted(out[1:], key=lambda x: int(x[-1])):
        f.write('\t'.join(line)+'\n')
        
