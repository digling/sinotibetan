# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-30 15:10
# modified : 2015-06-30 15:10
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-06-30"

from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase

db = LexiBase(
        'sinotibetan',
        dbase='sqlite/sinotibetan.sqlite3',
        url = 'sinotibetan.sqlite3'
        )

def clean(word):

    st = list(zip('0123456','⁰¹²³⁴⁵⁶')) + [
            (']a',''),
            (' ',''),
            ('[',''),
            (']',''),
            ("'",'ʰ'),
            ('ๅ','ɿ'),
            ('ῃ','ŋ̍'),
            ]
    if ',' in word: 
        word = word.split(',')[0]

    for s,t in st:
        word = word.replace(s,t)
    tks = ipa2tokens(word, expand_nasals=True, 
            merge_vowels=False, 
            semi_diacritics='sɕʑzʃʒʂʐṣh'
            )
    return tks

# determine those entries where tokens are missing
for k in db:
    oe = db[k,'entry_in_source']
    ipa = db[k,'ipa']
    tokens = db[k,'tokens']

    if not tokens and ipa:
        tokens = clean(ipa)

    if 'ๅ' in ipa or 'ῃ' in ipa or 'ṣ' in ipa or ',' in ipa:
        tokens = clean(ipa)
    
    if tokens:
        if type(tokens) == list:
            tokens = ' '.join(tokens)

        db[k][db.header['tokens']] = tokens
        


db.create('sinotibetan')
