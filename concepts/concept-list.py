# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-04-14 11:02
# modified : 2015-04-14 11:02
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-04-14"

from lingpyd import *
import wget
import os
import datetime
import sys

# get the downloadlist
if os.path.isfile('sinotibetan.concepts.tsv'):
    os.rename('sinotibetan.concepts.tsv',
            'backup/sinotibetan.concepts.tsv-backup-'+\
                    str(datetime.datetime.now()).split('.')[0])
wget.download(
    'http://tsv.lingpy.org/triples/triples.py?file=sinotibetan&remote_dbase=sinotibetan&unique=CONCEPT&content=html',
    out='sinotibetan.concepts.tsv'
    )

concepts = csv2list(



