from lingpy import *
from pystdb import *
from collections import defaultdict

wl = Wordlist('Bunan-wordlist.tsv')
stb = load_sinotibetan(remote=True)

stb.add_data(wl)
stb.update('sinotibetan')

