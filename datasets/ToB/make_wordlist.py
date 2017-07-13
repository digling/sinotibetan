from lingpy import *

wl1 = csv2list('Kulung.mapped.tsv', strip_lines=False)
wl2 = csv2list('Kulung.tsv', strip_lines=False)
wld = {k[0]: k for k in wl2[1:]}

D = {
        0: [
            'doculect',
            'concept',
            'gloss_in_source',
            'ipa',
            'tokens',
            'source',
            'cogid',
            'tbl_id',
            'note',
            ]
        }

def clean_string(string):
    subs = {
            ':' : 'ː',
            '-' : '',
            'ch': 'tʃʰ',
            'kh': 'kʰ',
            'ph': 'pʰ',
            'N': 'ŋ',
            'c': 'tʃ',
            'th': 'tʰ',
            ' ': '_',
            'y': 'j'
            }
    return [y for y in [subs.get(x, x) for x in ipa2tokens(string.replace(' ',
        '_'), semi_diacritics='sh',
            merge_geminates=False, merge_vowels=False)] if y]

count = 1
for line in wl1[1:]:
    if len(line) == 6:
        if line[4].strip():
            D[count] = [
                    'Kulung',
                    line[1],
                    wld[line[4]][3] + ' ({0})'.format(wld[line[4]][5]) if \
                            wld[line[4]][5].strip() else '',
                    wld[line[4]][2],
                    clean_string(wld[line[4]][2]),
                    'Tolsma1999',
                    '0',
                    line[3],
                    'Nepali: {0} (Tolsma1999)'.format(wld[line[4]][4]) if wld[line[4]][4].strip() else ''
                    ]
            count += 1
wl = Wordlist(D)
from pystdb import *
stb = load_sinotibetan(remote=True)
stb.add_data(wl)
for k in stb:
    if stb[k, 'doculect'] in ['Chepang', 'Rongpo']:
        if 'j' in stb[k, 'tokens'] or 'c' in stb[k, 'tokens']:
            tks = []
            for t in stb[k, 'tokens']:
                if t == 'j':
                    tks += ['dʒ']
                elif t == 'c':
                    tks += ['tʃ']
                else:
                    tks += [t]
            stb[k, 'tokens'] = tks
stb.update('sinotibetan')
