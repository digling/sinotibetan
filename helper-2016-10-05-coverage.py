from pystdb import *
from lingpy import *

wl = load_sinotibetan(tsv=True)
concepts = wl.concepts
btext = '# Missing words in the STDB Database\n'
texts = []
for t in wl.taxa:
    text = '## Missing words for {0}\n'.format(t)
    _text = []
    words = wl.get_dict(taxa=t)
    for c in concepts:
        if c not in words:
            _text += [c]
    text += '* {0} concepts are missing\n'.format(len(_text))
    text += '\n'.join(['* {0}'.format(t) for t in _text])+'\n'
    if _text:
        texts += [text]
with open(stdb_path('stats', 'missing.md'), 'w') as f:
    f.write(btext+'\n'.join(texts))

