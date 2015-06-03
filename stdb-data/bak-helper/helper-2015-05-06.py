# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-06 10:10
# modified : 2015-05-06 10:10
"""
Helper creates a list of Meta-Data for the languages taken from TBL.
"""

__author__="Johann-Mattis List"
__date__="2015-05-06"

from lingpyd import *
import json

def clean_taxname(word):
    
    word = word.replace(' ','_')
    return ''.join([x for x in word if x not in '()[]-.'])

tbl = csv2list('tbl.languages.tsv', strip_lines=False)
stdb = Wordlist('stdb-2015-05-06.tsv')

D = {}
for line in tbl:

    tmp = dict(
            taxon_name = clean_taxname(line[1]),
            iso = line[0],
            taxon_name_in_source = line[1],
            taxon_short_name = line[2].split(' ')[0],
            taxon_id_in_source = line[2].split(' ')[1],
            classification_in_source = line[3],
            number_of_entries_in_source = line[4]
            )
    tmp['source'] = 'Huang1992'
    tmp['subgroup'] = line[3].split(' - ')[1]
    tmp['url'] = "https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/source/TBL"
    
    try:
        tmp['entries'] = len(stdb.get_dict(taxon=clean_taxname(line[1])))
        D[clean_taxname(line[1])] = tmp
    except:
        print('Taxon {0} is not in STDB.'.format(line[1]))

# add the other stuff, also where we don't have the metadata
for t in stdb.taxa:
    if t not in D:
        tmp = dict(
                taxon_name = '',
                iso = '',
                taxon_name_in_source = '',
                taxon_short_name = '',
                taxon_id_in_source = '',
                classification_in_source = '',
                number_of_entries_in_source = ''
                )
        tmp['source'] = ''
        tmp['subgroup'] = stdb[stdb.get_list(taxon=t, flat=True)[0],'subgroup']
        tmp['url'] = ""
        
        try:
            tmp['entries'] = len(stdb.get_dict(taxon=t))
            D[t] = tmp
        except:
            print('Taxon {0} is not in STDB.'.format(line[1]))



with open('metadata.json','w') as f:
    f.write(json.dumps(D, indent=2))

