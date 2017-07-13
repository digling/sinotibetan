from lingpy import *

header = ['language', 'gloss', 'ipa', 'segments', 'source']
with open('Bunan_Dictionary.txt') as f:
    ingloss = False
    D = {}
    idx = 1
    word, gloss, tmp = '', '', {}
    for i, line in enumerate(f):
        if line.startswith('\\lx'):
            ingloss = True
            tmp = {}

        if not line.strip() and ingloss:
            ingloss = False
            D[idx] = dict(
                    ipa = word,
                    segments = ' '.join(ipa2tokens(word,
                        semi_diacritics='ɕʑszʂʐ')) if word else '',
                    source = 'Widmer2014',
                    gloss = gloss,
                    language = 'Bunan',
                    )
            for k, v in tmp.items():
                D[idx][k] = v

            idx += 1
            word, gloss, tmp = '', '', {}

        if ingloss:
            if line.startswith('\\lx'):
                word = ' '.join(line.strip().split(' ')[1:])
            elif line.startswith('\\ge'):
                gloss = ' '.join(line.strip().split(' ')[1:])
            else:
                first, *rest = line.strip().split(' ')
                tmp[first[1:]] = ' '.join(rest)
                if first[1:] not in header:
                    header += [first[1:]]

with open('bunan.tsv', 'w') as f:
    f.write('ID\t'+'\t'.join([h.upper() for h in header])+'\n')
    for i in sorted(D):
        f.write(str(i)+'\t'+'\t'.join([str(D[i].get(k, '')) for k in header])+'\n')
