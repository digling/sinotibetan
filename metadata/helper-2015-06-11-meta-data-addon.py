# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-11 11:37
# modified : 2015-06-11 11:37
"""
Add the data from the Cihui as metadata to the stdb.
"""

__author__="Johann-Mattis List"
__date__="2015-06-11"

from lingpyd import *
import json

# load metadata
with open('metadata.json') as f:
    meta = json.loads(f.read())

# load the meta-list of bjdx
taxa = csv2list('../datasets/BeijingDaxue/beida.taxa', strip_lines=False)

# start adding the relevent information
tags=["entries","url","number_of_entries_in_source", "taxon_short_name","taxon_name_in_source","taxon_id_in_source", "subgroup","source","iso","taxon_name","concepts"]

for line in taxa[1:]:
    meta[line[1]] = {}
    for t in tags:
        meta[line[1]][t] = ''

    meta[line[1]]['subgroup'] = 'Sinitic' 
    meta[line[1]]['classification'] = 'Sinitic.'+line[2]+'.'+line[1]
    meta[line[1]]['source'] = 'BeijingDaxue1964'
    meta[line[1]]['number_of_entries_in_source'] = 905
with open('meta.modified.json', 'w') as f:
    f.write(json.dumps(meta, indent=2))
