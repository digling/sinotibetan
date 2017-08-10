from lingpy import *
from pystdb import *

concepts = stdb_concepts()
db = load_sinotibetan()

burmese = csv2list(stdb_path('datasets', 'burmese', 
    'Missing concepts Burmese and Old Burmese - Sheet1.tsv'), strip_lines=False)
oburm = [line for line in burmese if 'Old_Burmese' in line[2]]
nburm = [line for line in burmese if line[2].strip() == 'Burmese']
#nburm2newb = dict([(line[1], line[3]) for line in nburm])
oburmc = [line[1] for line in oburm if line[3].strip()]
nburm = [line for line in nburm if line[1] not in oburmc]

# add old burmese
D = {}
idx = 1
for line in oburm:
    concept = line[1]
    if concept not in concepts:
        concept = concept[:-2]
        if concept not in concepts:
            print(concept)
            raise
    tokens = line[3]
    if tokens.strip():
        language = 'Old_Burmese'
        D[idx] = [language, concept, tokens.replace(' ',''), tokens, 'Hill2016', '']
        idx += 1
for line in nburm:
    concept = line[1]
    if concept not in concepts:
        concept = concept[:-2]
        if concept not in concepts:
            print(concept)
            raise
    tokens = line[3]
    if tokens.strip():
        language = 'Old_Burmese'
        D[idx] = [language, concept, tokens.replace(' ',''), tokens, 'Hill2016', '!Written Burmese']
        idx += 1

D[0] = ['doculect', 'concept', 'ipa', 'tokens', 'source', 'note']
db.add_data(Wordlist(D))

db.add_entries('concepticon_id', 'concept', lambda x: concepts.get(x,
    {}).get('CONCEPTICON_ID'))
db.add_entries('tbl_id', 'concept', lambda x: concepts.get(x,
    {}).get('TBL_ID'))
db.create('sinotibetan')

