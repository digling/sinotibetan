from lingpy import *

stdb = csv2list('STDB-2016-250.tsv', strip_lines=False)
bjdx = csv2list('BeijingDaxue-1964-905.tsv')
bjdxd = {k[10]: k for k in bjdx[1:]}
stdbd = {k[5]: k for k in stdb}
liud = {k[4]: k for k in csv2list('Liu-2007-201.tsv')}
houd = {k[1]: k for k in csv2list('Hou-2004-180.tsv')}


with open('mappings-all.tsv', 'w') as f:
    f.write('\t'.join([
        'NUMBER',
        'GLOSS',
        'TBL_ID',
        'CONCEPTICON_ID',
        'BJDX_ID',
        'BJDX_GLOSS',
        'BJDX_CHINESE',
        'LIU_ID',
        'LIU_GLOSS',
        'LIU_CHINESE',
        'HOU_ID',
        'HOU_GLOSS',
        'HOU_CHINESE'
        ])+'\n')
    for line in stdb[1:]:
        if line[5] in bjdxd:
            b1, b2, b3 = (
                    bjdxd[line[5]][1], 
                    bjdxd[line[5]][8],
                    bjdxd[line[5]][2]
                    )
        else:
            b1, b2, b3 = '', '', ''

        if line[5] in liud:
            l1, l2, l3 = (
                    liud[line[5]][1], 
                    liud[line[5]][3],
                    liud[line[5]][2]
                    )
        else:
            l1, l2, l3 = '', '', ''
        if line[5] in houd:
            h1, h2, h3 = (
                    houd[line[5]][3],
                    houd[line[5]][4], 
                    houd[line[5]][5],
                    )
        else:
            h1, h2, h3 = '', '', ''
        f.write('\t'.join([
            line[1], line[2], line[4], line[5], 
            b1, b2, b3, l1, l2, l3, h1, h2, h3, '???' if not h1 and not l1 and not
            b1 else ''])+'\n')



with open('mappings.tsv', 'w') as f:
    for line in stdb[1:]:
        if line[5] in bjdxd:
            f.write('\t'.join([
                line[0],
                line[1],
                line[2],
                line[4],
                line[5],
                bjdxd[line[5]][1],
                bjdxd[line[5]][2], 
                bjdxd[line[5]][8],
                'BeijingDaxue1964'])+'\n')
        elif line[5] in liud:
            f.write('\t'.join([
                line[0],
                line[1],
                line[2],
                line[4],
                line[5],
                liud[line[5]][1],
                liud[line[5]][3], 
                liud[line[5]][2],
                'Liu2007'])+'\n')
        elif line[5] in houd:
            f.write('\t'.join([
                line[0],
                line[1],
                line[2],
                line[4],
                line[5],
                houd[line[5]][3],
                houd[line[5]][4], 
                houd[line[5]][5],
                'Hou2004'])+'\n')


        else:
            f.write('\t'.join([
                line[0],
                line[1],
                line[2],
                line[4],
                line[5],
                '',
                '', 
                '',
                '???'])+'\n')
