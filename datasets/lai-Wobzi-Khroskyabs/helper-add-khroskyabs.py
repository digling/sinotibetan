from lingpy import *
from pystdb import *

data = csv2list('Wobzi-Khroskyabs.csv', strip_lines=False)
D = {}
stb = load_sinotibetan(remote=True)

idx = 1
for line in data:
    concept = line[1].strip()
    word = line[2].strip()
    if word:
        tks = ipa2tokens(word.replace(
            '|', '').replace('-', '+').replace(' ','_'), merge_vowels=False,
                semi_diacritics='sʃʂɕzʒʐʑ')
        note = line[3].strip()
        cid = line[6].strip()
        D[idx] = [concept, 'Wobzi_Khroskyabs', word, tks, 0, 'Lai2016', cid, note]
        idx += 1
D[0] = ['concept', 'doculect', 'ipa', 'tokens', 'cogid', 'source',
        'concepticon_id', 'note']
stb.add_data(Wordlist(D))

wl = Wordlist(D)
#stb.add_data(wl)
stb.update(table='sinotibetan')
#stb.create('sinotibetan')
print(idx / 250)
