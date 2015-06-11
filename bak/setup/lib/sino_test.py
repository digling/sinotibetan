# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-01-21 13:41
# modified : 2015-01-21 13:41
"""
Script loades the database remotely and allows to update it in several
scripting steps.
"""

__author__="Johann-Mattis List"
__date__="2015-01-21"

from lingpyd.plugins.lpserver.lexibase import *

db = LexiBase('sinotibetan',dbase='../sqlite/sinotibetan.sqlite3',
        )
        



