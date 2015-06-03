# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-05 10:29
# modified : 2015-03-05 10:29
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-03-05"

from lingpyd import *
from lingpyd.plugins.chinese.sinopy import clean_chinese_ipa
from lingpyd.plugins.lpserver.lexibase import LexiBase
from sys import argv
import sys

if len(argv) <= 1:
    print("no doculect added")
    sys.exit()
else:
    doculect = argv[1]

stb = LexiBase('sinotibetan', dbase='sinotibetan.sqlite3',
        url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3')

# get owids for concept
c2o = {}
for k in stb:
    concept = stb[k,'concept']
    owid = stb[k,'omegawiki']
    
    if concept not in c2o:
        c2o[concept] = owid


doculects = doculect.split(',')
for doculect in doculects:
    # make a template
    D = {}
    idx = 1
    D[0] = ['doculect','concept','omegawiki']
    
    for k in stb.concepts:

        D[idx] = [doculect,k,c2o[k]]
        idx += 1
    
    wl = Wordlist(D)
    
    stb.add_data(wl)
stb.create('sinotibetan')



