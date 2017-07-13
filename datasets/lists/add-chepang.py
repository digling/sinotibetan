from lingpy import *
from pystdb import *
from collections import defaultdict

csv = csv2list('Vanbik2014.tsv', strip_lines=False)
D = {0: ['concept', 'doculect', 'gloss_in_source', 'ipa', 'tokens', 'source',
    'note', 'concepticon_id']}
k = 1
for row in csv[1:]:
    note = '[full entry: '+row[6]+ ']'
    D[k] = [
            row[1],
            'Hakha_Chin',
            row[4],
            row[5],
            row[7],
            'VanBik2014',
            note,
            row[3]]
    k += 1
wl = Wordlist(D)
stb = load_sinotibetan(remote=True)

stb.add_data(wl)
stb.update('sinotibetan')

