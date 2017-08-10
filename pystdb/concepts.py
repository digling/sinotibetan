from lingpy import *
from pystdb import stdb_concepts, stdb_concepts, load_stedt
import os
from collections import defaultdict

def check_coverage(path, language):
    wl = load_stedt(path)
    falam = wl.get_list(col=language, flat=True)
    with open('tmp.tsv', 'w') as f:
        f.write('{0}\t{1}\n'.format('ID', 'ENGLISH'))
        for k in falam:
            concept = wl[k, 'concept']
            #if '(' in concept:
            #    concept = concept[:concept.index('(')]
            idx = wl[k, 'rn']
            if concept.strip():
                if wl[k, 'gfn']:
                    concept += ' ({0})'.format(wl[k, 'gfn'])
                f.write(idx+'\t'+concept+'\n')
    os.system('concepticon map_concepts tmp.tsv > tmp.mapped.tsv')
    csv = csv2list('tmp.mapped.tsv')
    #for i, line in enumerate(csv):
    #    if '(' in line[1]:
    #        idx = line[1].index('(')
    #        csv[i][1] = line[1][:idx]
        
    concepts = {k: v for k, v in stdb_concepts().items() if int(v['rank']) <
            227}
    cids = [c['concepticon_id'] for c in concepts.values()]
    vkg = defaultdict(list)
    for line in csv:
        print(line)
        if len(line) > 2:
            vkg[line[2]] += [line]
    common = [c for c in cids if c in vkg]
    for k in [x for x in concepts if concepts[x]['concepticon_id'] not in vkg]:
        print(k)

    print(len(common), '{0:.2f}'.format(len(common) / len(concepts)))
    with open(language+'.mapped.tsv', 'w') as f:
        f.write('\t'.join(
            [
                'NUMBER',
                'ENGLISH',
                'CONCEPTICON_ID',
                'TBL_ID',
                'SRCID',
                'SRCGLOSS'])+'\n')
        for k, val in sorted(concepts.items()):
            out = [
                    val['number'],
                    val['gloss'],
                    val['concepticon_id'],
                    val['tbl_id'],
                    ]
            if val['concepticon_id'] in vkg:
                if len(vkg[val['concepticon_id']]) > 1:
                    f.write('#<<<\n')
                for line in vkg[val['concepticon_id']]:
                    hout = [h for h in out] + [line[0], line[1]]
                    f.write('\t'.join(hout)+'\n')
                if len(vkg[val['concepticon_id']]) > 1:
                    f.write('#>>>\n')

            else:
                f.write('\t'.join(out)+'\t\t???\n')
                

