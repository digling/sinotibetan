from lingpy import *
from pystdb import *
from collections import defaultdict

stb = load_sinotibetan(remote=True)
source = 'Caughley2000'

wl = Wordlist('byangsi.tsv')
wl.add_entries('source', 'ipa', lambda x: 'Sharma2003')
stb.add_data(wl)

wl = Wordlist('rongpo.tsv')
wl.add_entries('source', 'ipa', lambda x: 'Sharma2003a')
stb.add_data(wl)
stb.update('sinotibetan')

