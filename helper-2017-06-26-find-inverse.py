from pystdb import *
from pyburmish.dataset import Dataset
import json

stdb = load_sinotibetan(remote=False, tsv=True)

tbl = Wordlist(Dataset('Huang1992').raw('tbl2.tsv'))
concepts = {}
visited = []
#for k in tbl:
#    try:
#        tblid = tbl[k, 'srcid'].split('.')[0]
#        if tblid in visited:
#            pass
#        else:
#            concepts[tblid] = tbl[k, 'concept']
#            visited += [tblid]
#    except:
#        pass
    
stdb2tbl = csv2list(stdb_path('concepts', 'STDB-2016-250.tsv'))

conv = {x[2]: str(int(x[4])) for x in stdb2tbl[1:]}
sources = json.load(open(stdb_path('metadata', 'metadata.json')))


mapper = {
        'Achang_Longchuan':  'Achang (Longchuan)',
        'Atsi' : "Atsi [Zaiwa]",
        "Bola" : "Bola (Luxi)",
        "Darang_Taraon": "Darang [Taraon]",
        "Lashi" : "Leqi (Luxi)",
        "Maru" : "Langsu (Luxi)",
        "Motuo_Menba" : "Motuo Menba",
        "Rangoon": "Burmese (Rangoon)",
        "rGyalrong_Maerkang": "rGyalrong (Maerkang)",
        "Tibetan_Alike": "Tibetan (Alike)",
        "Tibetan_Batang": "Tibetan (Batang)",
        "Tibetan_Lhasa" : "Tibetan (Lhasa)",
        "Tibetan_Xiahe": "Tibetan (Xiahe)",
        "Xiandao": "Achang (Xiandao)",
        "Zhaba_Daofu_County": "Zhaba (Daofu County)",
        
        }

def modify(string):
    for s, t in [['ʨ', 'tɕ'], ['ʈʂ', 'tʂ'], ['◦', ''],['ʨʰ', 'tɕh'], ['ʰ', 'h'], ['ʦ', 'ts'], ['|', ''], [' ', '']]:
        string = string.replace(s, t)
    return string

problems = []
idx = 1
for l in stdb.cols:
    if sources[l]['source'] == 'Huang1992':
        words = stdb.get_list(col=l, flat=True)
        alternative = tbl.get_dict(col=mapper.get(l, l), flat=True)
        for w in words:
            concept = stdb[w, 'concept']
            ipa = stdb[w, 'ipa']
            converted = alternative[conv.get(concept)]
            linked = False
            reflexes = [modify(tbl[c, 'ipa']) for c in converted]
            if ipa not in reflexes and modify(ipa) not in reflexes:
                print(idx, l, concept, ipa, reflexes, conv.get(concept, '?'))
                problems += [(str(idx), str(w), l, concept, ipa, ', '.join(reflexes), conv.get(concept,
                    '?'))]
                idx += 1
with open('errors.tsv', 'w') as f:
    f.write('COUNT\tWORD_ID\tLANGUAGE\tCONCEPT\tIPA\tSTEDT\tTBL_ID\n')
    for line in problems:
        f.write('\t'.join(line)+'\n')
    
                
