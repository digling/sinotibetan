from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase
import re

db = LexiBase(
        'sinotibetan',
        dbase = 'sinotibetan.sqlite3',
        url = 'http://tsv.lingpy.org/triples/sinotibetan.sqlite3'
        )

def uppertones(string):

    for a,b in zip('1234567','¹²³⁴⁵⁶⁷'):
            string = string.replace(a,b)
    
    return string

wl = Wordlist('caijia-addons.tsv')
wl.add_entries('tokens', 'ipa', lambda x: 
        ipa2tokens(
            uppertones(re.split(' = |/', x)[0].replace(
            ' ','').replace('[','').replace(']','').replace("'",'ʰ')),
            expand_nasals=True,
            semi_diacritics = 'hɕ',
            merge_vowels=False,
            ) if x != '-' else ''
        )

for c in wl.concept:
    if c not in db.concept:
        print(c)
db.add_data(wl)
wl = Wordlist('rucheng-addons.tsv')
wl.add_entries('tokens', 'ipa', lambda x: 
        ipa2tokens(
            uppertones(re.split(' = |/', x)[0].replace(
            ' ','').replace('[','').replace(']','').replace("'",'ʰ')),
            expand_nasals=True,
            semi_diacritics = 'hɕ',
            merge_vowels=False
            ) if x != '-' else ''
        )
db.add_data(wl)
db.create('sinotibetan')

