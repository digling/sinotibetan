from pystdb import *
from lingpy import *
from collections import defaultdict
from lingpy.compare.partial import Partial

wl = Wordlist('d_bed.tsv')
stdb = load_sinotibetan(tsv=True)

ob1 = wl.get_list(col='Old_Burmese', flat=True)
ob2 = stdb.get_list(col='Old_Burmese', flat=True)

for c in wl.rows:
    if c not in stdb.rows:
        print(c)

ob1d = defaultdict(list)
ob2d = defaultdict(list)
for idx in ob1:
    c, f, t = wl[idx, 'concept'], wl[idx, 'ipa'], wl[idx, 'tokens']
    if c in ob1d:
        pass #print(c)
    ob1d[c] = [(idx, f)]
#print('---')

for idx in ob2:
    c, f, t = stdb[idx, 'concept'], stdb[idx, 'ipa'], stdb[idx, 'tokens']
    if c in ob2d:
        pass #print(c)
    ob2d[c] += [(idx, f)]

matcher = {}
# following code to identify matches
for c, v in ob1d.items():
    if c in ob2d:
        if len(v) == len(ob2d[c]) and len(v) == 1:
            matcher[v[0][0]] = ob2d[c][0][0]
        else:
            pass
            #-for val in v:
            #-    print(c, val[0], val[1])
            #-print('---')
            #-for val in ob2d[c]:
            #-    print(c, val[0], val[1])
            #-print('***')

unmatched = []
for c, v in ob2d.items():
    if c in ob1d:
        pass
    else:
        for x in v:
            unmatched += [x[0]]


explicit = {
    7533: 31265,
    7306: 31159,
    7308: 31160,
    7175: 31094,
    7177: 31095,
    7501: 31250,
    7499: 31249,
    7503: 31251,
    7447: 31227,
    7449: 31228,
    7334: 31173,
    7336: 31174,
    7133: 31074,
    7131: 31073,

        }
matcher.update(explicit)
blacklist = []
for idx in ob2:
    if idx not in matcher.values() and idx not in unmatched:
        blacklist += [idx]

# now that we have all relevant data, we need to compare the cognate sets
# print(max([int(stdb[idx, 'cogid']) for idx in stdb]))

# cogid range should be 7000+
part = Partial(wl)
part.add_cognate_ids('cogids', 'strictid', idtype='strict')

# compute a matcher of cognate ids
burm2stdb = {}
ncid = 8000
for idx in part:
    nidx = matcher.get(idx)
    tid = part[idx, 'strictid']
    if nidx and nidx not in burm2stdb:
        oid = stdb[nidx, 'cogid']
        burm2stdb[tid] = oid
    else:
        if tid in burm2stdb:
            pass
        else:
            burm2stdb[tid] = str(ncid)
            ncid += 1
D = {0: ['doculect', 'concept', 'gloss_in_source', 'concepticon_id',
    'morpheme_structure', 'cogids', 'cogid', 'alignment', 'ipa', 'tokens', 'note',
    'source']}
for idx, d, c, oc, cid, mrp, cids, cgid, alm, ipa, tks, note in iter_rows(part,
        'doculect', 'concept', 'original_concept', 'concepticon_id',
        'morphemes', 'cogids', 'strictid', 'alignment', 'ipa', 'tokens',
        'note'):
    cogid = burm2stdb[cgid]
    if d != 'Old_Burmese':
        D[idx] = [
                d, c, oc, cid, mrp, cids, cogid, alm, ipa, tks, note,
                'Huang1992']
stdbn = load_sinotibetan(remote=True)
stdbn.add_data(Wordlist(D))
stdbn.update('sinotibetan')
    
