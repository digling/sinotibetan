# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-02-10 11:14
# modified : 2015-02-10 11:14
"""
Script is used to clean ganzhou-data.
"""

__author__="Johann-Mattis List"
__date__="2015-02-10"

from lingpyd import *
from lingpyd.plugins.chinese.sinopy import clean_chinese_ipa
from lingpyd.plugins.lpserver.lexibase import LexiBase

# load stb data (today's status)
stb = LexiBase('sinotibetan', dbase='../../sqlite/sinotibetan.sqlite3',
        url='http://tsv.lingpy.org/triples/sinotibetan.sqlite3')

        #Wordlist('sinotibetan-2015-02-10.tsv')

# get owids and concetps
owid2concept = {}
visited = []
for k in stb:
    concept = stb[k,'concept']
    owid = stb[k,'omegawiki']

    if concept == 'to lick':
        stb[k][stb.header['omegawiki']] = '1510483'
    elif concept == 'to bark':
        stb[k][stb.header['omegawiki']] = '5444'
    
    if (concept,owid) not in visited:
        try:
            owid2concept[owid] += [concept]
        except:
            owid2concept[owid] = [concept]
        visited += [(concept,owid)]

# check for consistency
for k,v in owid2concept.items():
    if len(v) > 1:
        print('multends!',k,'/'.join(v))

# load ganzhou
gzh = csv2list('ganzhou-merged.tsv')

# clean entries
gzhout = {}
idx = max(stb)+1

addconcepts = dict([
        ('194', 'the animal'),
        ('6078', 'at'),
        ('6039', 'to burn (intransitive)'),
        ('568', 'the child (young human'),
        ('828398', 'the claw'),
        ('5988', 'dull'),
        ('5619', 'fat (obese)'),
        ('6076', 'if'),
        ('6077', 'in'),
        ('5873', 'knife'),
        ('5936', 'now'),
        ('5844', 'with'),
        ('6070', 'wipe'),
        ('514093', 'because'),
        ])
for line in gzh[1:]:

    # try to find owid
    owid = line[3]
    
    if owid not in owid2concept:
        if owid in addconcepts:
            concept = addconcepts[owid]
        else:
            concept = '?'
            print(owid,line[1])
    else:
        concept = '/'.join(owid2concept[owid])

    ipas = line[2].split(',')
    for ipa in ipas:

        new_ipa = clean_chinese_ipa(ipa)
        tokens = ' '.join(ipa2tokens(new_ipa, expand_nasals=True,
                merge_vowels=False))
        gzhout[idx] = [line[1]+ ' (' + line[0]+')', line[2], line[3], concept,
                new_ipa, tokens]
        idx += 1


# try to re-assign values for ganzhou
ganzhou = stb.get_list(doculect='Ganzhou')

#with open('ganzhou_cleaned.tsv', 'w') as f:
#    f.write('ID\tDOCULECT\tGLOSS_IN_SOURCE\tENTRY_IN_SOURCE\tOMEGAWIKI\tCONCEPT\tIPA\tTOKENS\n')
#    for k,v in sorted(gzhout.items()):
#        f.write(str(k)+'\tGanzhou\t'+'\t'.join(v)+'\n')
#
wl = Wordlist('ganzhou_cleaned.tsv')

stb.add_data(wl)
stb.create('sinotibetan', ignore=ganzhou)

