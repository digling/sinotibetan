from lingpy import *

csv1 = csv2list('maps.tsv', strip_lines=False)
csv2 = csv2dict('vanbik-data.tsv', strip_lines=False)

out = []
for line in csv1[1:]:
    vb = line[5]
    vg = line[6]
    print(vb, line)
    entry = csv2[vb][1]
    tks = ' '.join(ipa2tokens(entry.split()[0]))
    out += [[
        line[0], line[1], line[3], line[4], vg, entry, tks, 'VanBick2014']]
with open('Vanbik-2014-STDB.tsv', 'w') as f:
    f.write('\t'.join([
        'NUMBER', 'concept', 'tbl_id', 'concepticon_id',
        'gloss_in_source', 'ipa', 'tokens', 'source'])+'\n')
    for line in out:

        f.write('\t'.join(line)+'\n')
