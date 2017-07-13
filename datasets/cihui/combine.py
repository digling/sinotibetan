from lingpy import *
from pycddb.dataset import Dataset
from pyconcepticon import api
from pystdb import stdb_concepts
from collections import defaultdict


# load the merging list
con = api.Concepticon()
stdb = api.Conceptlist.from_file('STDB-2016-250.tsv')
liu = con.conceptlists['Liu-2007-201']
hou = con.conceptlists['Hou-2004-180']
hui = con.conceptlists['BeijingDaxue-1964-905']

zihui = Dataset('BeijingDaxue1962').characters
zh2d = defaultdict(dict)
for idx, char, dial, seg in iter_rows(zihui, 'character', 
        'doculect', 'segments'):
    zh2d[char][dial] = ' '.join(seg)

liu2con = {c.number: c.english for c in liu.concepts.values()}
liu2con2 = {c.concepticon_id: c.english for c in liu.concepts.values()}
hou2con = {c.number: c.gloss for c in hou.concepts.values()}
hou2con2 = {c.concepticon_id: c.gloss for c in hou.concepts.values()}
hui2con = {c.number: c.gloss for c in hui.concepts.values()}



dialects = [
        'Beijing',
        'Xiamen',
        'Fuzhou',
        'Nanchang',
        'Meixian',
        'Guangzhou',
        ]


maps = api.Conceptlist.from_file('mappings-2017-05-04.tsv')

liudb = Dataset('Liu2007').words
houdb = Dataset('Hou2004').words
beidb = Wordlist('beijing-daxue-1964-cihui.tsv', row='beida_id')

dialects = [k for k in beidb.cols if k in houdb.cols and k in liudb.cols]
for k in dialects:
    print(k)

D = {0: [
        'DOCULECT',
        'CONCEPT',
        'CONCEPTICON_ID',
        'TBL_ID',
        'GLOSS_IN_SOURCE',
        'CHINESE_GLOSS_IN_SOURCE',
        'ALT_IPA',
        'ALT_GLOSS',
        'ALT_SOURCE',
        'ALT_CHARS',
        'ALT_CHINESE_GLOSS',
        'IPA',
        'HANZI',
        'SOURCE', 
        'TOKENS']}
this_id = 1
for d in dialects:
    tmp = liudb.get_dict(col=d)
    tmp2 = houdb.get_dict(col=d)
    tmp3 = beidb.get_dict(col=d)
    count = 1

    with open(d+'.tsv', 'w') as f:
        for key, concept in maps.concepts.items():
            sources, words, chars, glosses, cglosses = [], [], [], [], []
            alt_ipa, alt_gloss, alt_source, alt_chars, alt_cgloss = [], [], [], [], []
            if concept.attributes['bjdx_id']:
                idxs = tmp3[concept.attributes['bjdx_id']]
                hanzis = [beidb[idx, 'hanzi'] for idx in idxs]
                readings = [beidb[idx, 'tokens'] for idx in idxs]

                for a, b in zip(hanzis, readings):
                    sources += ['BeijingDaxue1964']
                    words += [b]
                    chars += [a]
                    glosses += [concept.attributes['bjdx_gloss']]
                    cglosses += [concept.attributes['bjdx_chinese']]

            if concept.attributes['hou_id']:
                idxs = tmp2[concept.attributes['hou_gloss']]
                hanzis = [houdb[idx, 'characters'] for idx in idxs]
                readings = [houdb[idx, 'segments'] for idx in idxs]
                for a, b in zip(hanzis, readings):
                    if words:
                        alt_source += ['Hou2004']
                        alt_ipa += [''.join(b)]
                        alt_chars += [a]
                        alt_gloss += [concept.attributes['hou_gloss']]
                        alt_cgloss += [concept.attributes['hou_chinese']]
                    else:
                        sources += ['Hou2004']
                        words += [b]
                        glosses += [concept.attributes['hou_gloss']]
                        cglosses += [concept.attributes['hou_chinese']]



            if concept.attributes['liu_id']:
                idxs = tmp[concept.attributes['liu_gloss']]
                hanzis = [liudb[idx, 'characters'] for idx in idxs]
                readings = [liudb[idx, 'segments'] for idx in idxs]
                for a, b in zip(hanzis, readings):
                    if words:
                        alt_source += ['Liu2007']
                        alt_ipa += [''.join(b)]
                        alt_chars += [a]
                        alt_gloss += [concept.attributes['liu_gloss']]
                        alt_cgloss += [concept.attributes['liu_chinese']]
                    else:
                        sources += ['Liu2007']
                        words += [b]
                        glosses += [concept.attributes['liu_gloss']]
                        cglosses += [concept.attributes['liu_chinese']]


            if words:
                print(words)
                for i, (g, c, w, c, s) in enumerate(zip(
                    glosses, cglosses, words, chars, sources)):
                    if i == 0:
                        asr, ai, ac, ag, acc = (
                                ' / '.join(alt_source),
                                ' / '.join(alt_ipa),
                                ' / '.join(alt_chars),
                                ' / '.join(alt_gloss),
                                ' / '.join(alt_cgloss)
                                )
                    else:
                        asr, ai, ac, ag, acc = '', '', '', '', ''

                    D[this_id] = [d, concept.gloss, concept.concepticon_id, 
                            concept.attributes['tbl_id'], 
                            g, 
                            c,
                            ai, ag, asr, ac, acc,
                            ''.join(w),
                            c,
                            s, w]
                    this_id += 1

wl = Wordlist(D)
# get partial cognates from current characters
conv = {}
cogid = 1
for idx, concept, chars in iter_rows(wl, 'concept', 'hanzi'):
    for char in chars:
        if (concept, char) not in conv:
            if char not in ['!', '□']:
                conv[concept, char] = str(cogid)
                cogid += 1
            elif char == '!':
                conv[concept, char] = '?'
            else:
                conv[concept, char] = '0'


wl.add_entries('cogids', 'concept,hanzi', lambda x, y: ' '.join(
    [conv.get((x[y[0]], z), '0') for z in x[y[1]] if z != '!']
    ))

wl.output('tsv', filename='chinese-data', prettify=False, ignore='all')



                
            


        #if concept.attributes['source'] == 'Liu2007':
        #    for k in tmp[liu2con[concept.attributes['other_id']]]:
        #        print(concept.id, count, (concept.english or concept.gloss), liudb[k, 'value'], 
        #                ' '.join(liudb[k, 'segments']))
        #    count += 1
        #elif concept.concepticon_id in liu2con2:
        #    for k in tmp[liu2con2[concept.concepticon_id]]:
        #        print(concept.id, count, (concept.english or concept.gloss), liudb[k, 'value'], 
        #                ' '.join(liudb[k, 'segments']))
        #    count += 1

        #if concept.attributes['source'] == 'Hou2004':
        #    for k in tmp2[hou2con[concept.attributes['other_id']]]:
        #        print(concept.id, '*'+str(count), (concept.english or concept.gloss), houdb[k, 'value'], 
        #                ' '.join(houdb[k, 'segments']))
        #    count += 1
        #elif concept.concepticon_id in hou2con2:
        #    for k in tmp2[hou2con2[concept.concepticon_id]]:
        #        print(concept.id, '*'+str(count), (concept.english or concept.gloss),
        #                houdb[k, 'value'], 
        #                ' '.join(houdb[k, 'segments']))


