from pystdb import *
from lingpy import *

stdb = load_sinotibetan(remote=True, tsv=False)

errors = csv2list(stdb_path('dumps', 'corrections-2017-07-13.tsv'))

for line in errors:

    wid = int(line[1])
    stdb[wid, 'ipa'] = line[5]
    stdb[wid, 'tokens'] = ipa2tokens(line[5], semi_diacritics='hsʃ')
    stdb[wid, 'cogid'] = '0'
stdb.update('sinotibetan')
