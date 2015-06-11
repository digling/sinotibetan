# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-01 11:32
# modified : 2015-04-01 11:32
"""
Utility functions to access the remote db and update it.
"""

__author__="Johann-Mattis List"
__date__="2015-04-01"

from lingpyd import *
from lingpyd.plugins.lpserver import lexibase as lb

# get remote db
def get_sinotibetan(remote=True):
    
    if not remote:
        url = False
    else:
        url = 'http://tsv.lingpy.org/triples/sinotibetan.sqlite3'

    db = lb.LexiBase('sinotibetan', dbase='sinotibetan.sqlite3',
            url=url)

    return db

