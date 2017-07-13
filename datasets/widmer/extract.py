from lingpy import *

mapped = csv2list('bunan-mapped.tsv', strip_lines=False)
mapper = {}
for line in mapped[1:]:
    if line[-1].strip():
        mapper[line[-2]] = dict(
                gloss_in_source = line[-3],
                concept = line[1],
                cid = line[2]
                )

data = csv2list('bunan.tsv')

D = {0: ['language', 'concept', 'ipa', 'tokens', 'source', 'gloss_in_source',
    'note', 'pos']}
idx = 1
for i, line in enumerate(data[1:]):
    bid = line[0]
    if bid in mapper:
        bgl = line[2]
        bipa = line[3]
        bsgs = line[4]
        for s in 'nŋ':
            for t in 'ɕʑsz':
                bsgs = bsgs.replace(s+t, s+' '+t)
        
        pos = line[8] if len(line) > 7 else ''
        ec = line[11] if len(line) > 7 else ''
        D[idx] = ['Bunan', mapper[bid]['concept'],
                bipa,
                bsgs,
                'Widmer2014',
                bgl,
                'Comment (by Widmer2014): «{0}»'.format(ec) if ec.replace(
                    '-', '').strip() else '',
                pos
                ]
        idx += 1
wl = Wordlist(D)
wl.output('tsv', filename='Bunan-wordlist', ignore='all', prettify=False)

