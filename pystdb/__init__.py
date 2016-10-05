from clldutils.dsv import UnicodeReader
import os
from pyconcepticon.api import Concepticon
from functools import partial
from lingpy._plugins.lpserver.lexibase import LexiBase
from lingpy import *
from collections import OrderedDict
import zipfile
from urllib import request
import zlib
from .data import url

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

def load_sinotibetan(remote=False, tsv=False):
    
    if tsv:
        return Wordlist(stdb_path('dumps', 'sinotibetan.tsv'),
                conf=stdb_path('conf', 'wordlist.rc'))
        
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
    
def backup(target='url'):
    """
    Function downloads dataset in actual version and saves it in zipped folder
    """
    
    
    time = rc('timestamp')
    if target == 'url':
        with request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with zipfile.ZipFile(stdb_path('dumps', 'bak-'+time+'.zip'), 
                'w',
                compression=zipfile.ZIP_DEFLATED
                ) as zf:
            zf.writestr('sinotibetan.tsv', data)
        

def download(target='url'):
    if target == 'url':
        with request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open(stdb_path('dumps', 'sinotibetan.tsv'), 'w') as f:
            f.write(data)

def history(limit):

    url='http://tsv.lingpy.org/triples/get_data.py?history=true&remote_dbase=sinotibetan.sqlite3&limit={0}'.format(limit)

    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        for line in data.split('\n'):
            print(line)
