from lingpy import *
from pystdb import *

mapped = csv2list('mapped.tsv', strip_lines=False)

mapper = dict([(line[1], line[2]) for line in mapped[1:]])
stb = load_sinotibetan(remote=True)
stb2 = load_sinotibetan(remote=False, tsv=True)
chin = csv2list('chin-hakha.tsv', strip_lines=False)
chind = dict([(k[0], k[1:]) for k in chin[1:]])
D = {}

cov = 1
for m, k in mapper.items():
    if m not in stb2.concepts:
        raise ValueError('not concept {0}'.format(m))

    if k:
        g, w = chind[k]
        if w.strip():
            print(cov, m, g, w)
            D[cov] = [m, g, 'Hakha', w, ipa2tokens(w), 0, 'StateznUnpublished']
            cov += 1
D[0] = ['concept', 'gloss_in_source', 'doculect', 'ipa', 'tokens', 'cogid',
        'source']
wl = Wordlist(D)
stb.add_data(wl)
#stb.create('sinotibetan')
print(cov / 250)
