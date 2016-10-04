from clldutils.dsv import UnicodeReader
import os
from pyconcepticon.api import Concepticon
from functools import partial
from lingpy._plugins.lpserver.lexibase import LexiBase
from collections import OrderedDict

def load_concepticon():

    concepticon = dict([
        (line['ID'], line) for line in Concepticon().conceptsets()
        ])

    return concepticon

def stdb_path(*comps):
    """
    Our data-path in CLICS.
    """
    return os.path.join(os.path.dirname(__file__), os.pardir, *comps)

def load_sinotibetan(remote=False):
    
    if not remote:
        db = LexiBase('sinotibetan', dbase=stdb_path('sqlite', 'sinotibetan.sqlite3'))
    else:
        db = LexiBase('sinotibetan', dbase=stdb_path('sqlite',
            'sinotibetan.sqlite3'), 
            url='sinotibetan.sqlite3')
    return db

def stdb_concepts():

    with UnicodeReader(stdb_path('concepts', 'concepts.tsv'), delimiter='\t') as reader:
        data = list(reader)
    concepts = {}
    for line in data[1:]:
        if line[1] in concepts:
            print(line[1])
        concepts[line[1]] = OrderedDict(zip(data[0], data[1:]))
    return concepts
    

