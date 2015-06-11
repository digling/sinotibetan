# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-11 08:30
# modified : 2015-06-11 08:30
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-06-11"

from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase
import json

# load the lexibase
db = LexiBase('sinotibetan', dbase='../sqlite/sinotibetan.sqlite3')

# load the current concept list
concepts = [line[2] for line in csv2list('../concepts/Jacques-2015-249.tsv',
    header=True)]

# load the meta-data file
with open('metadata.json') as f:
    meta = json.loads(f.read())

# write backup
with open('metadata.json.bak','w') as f:
    f.write(json.dumps(meta, indent=2))


missing = open('missing-data.tsv','w')
# start determining coverage
for t in db.taxa:
   
    if t in meta:
        #print("Calculating coverage for {0}...".format(t))
        idxs = db.get_list(taxon=t, flat=True)
        conc = [db[idx,'concept'] for idx in idxs]
        
        # get ipa for all (no empty entries allowed
        ipa_all = [db[i,'ipa'] for i in idxs if db[i,'ipa'] not in ('-','')]
        ipa_part = [db[i,'concept'] for i,c in zip(idxs,conc) if c in concepts and
                db[i,'ipa'] not in ('-','')]

        entries = len(ipa_all)
        coverage = len(set(ipa_part))
   
        meta[t]['entries'] = entries
        meta[t]['concepts'] = coverage
        meta[t]['coverage'] = int(100 * coverage / len(concepts) + 0.5)
        print(t,'\t',entries,'\t', coverage, '\t',
                '{0:.2f}'.format(coverage/len(concepts)))
        missing.write(
                t+'\t'+str(meta[t]['coverage'])+'\t'+','.join([x for x in concepts if x not in
                ipa_part])+'\n')

    else:
        print("[!] Missing meta-data for {0}".format(t))
missing.close()

with open('metadata.json', 'w') as f:
    f.write(json.dumps(meta, indent=2))

