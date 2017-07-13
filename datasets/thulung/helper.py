from pystdb import stdb_concepts, load_sinotibetan
from lingpy import *

thul = csv2list('thulung.tsv', strip_lines=False)
concepts = stdb_concepts()
count = 0
thulung = []
for line in thul:
    if line[0] in concepts:
        count += 1
        if line[2].strip():
            thulung += [(line[0], concepts[line[0]]['concepticon_id'], line[2],
                line[3], ' '.join(ipa2tokens(line[2])))]
    else:
        print(line[0])

D = {0: ['doculect', 'concept', 'concepticon_id', 'ipa', 'tokens', 'note']
    }
for i, line in enumerate(thulung):
    D[i+1] = ['Thulung'] + list(line)

stdb = load_sinotibetan(remote=True)
stdb.add_data(Wordlist(D))
stdb.update('sinotibetan')
