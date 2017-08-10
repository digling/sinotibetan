# add Bantawa and also the differences in cognates

from pystdb import load_sinotibetan
from lingpy import *

db = load_sinotibetan(remote=False)
wl = load_sinotibetan(remote=False, tsv=True)

D = {0: sorted(
    wl.header, key=lambda x: wl.header[x])}

for idx, cogid in iter_rows(wl, 'cogid'):
    
    
    if idx in db and db[idx, 'cogid'] != cogid:
        print(db[idx, 'doculect'], db[idx, 'concept'], db[idx, 'cogid'], cogid)
        db[idx, 'cogid'] = cogid
    elif idx not in db:
        D[idx] = wl[idx]

db.add_data(Wordlist(D))

# now add the new one
from pycalc.util import data_path
wl = Wordlist(data_path('Jongens2009', 'wordlist.tsv'))
wl.add_entries('cogid', 'ipa', lambda x: '0')
db.add_data(wl)
db.update('sinotibetan')
