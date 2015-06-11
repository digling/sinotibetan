from lib.sino import db
import lingpyd as lingpy


numbersup = '¹²³⁴⁵⁶⁰'
numbersdown = '₁₂₃₄₅₆₀'

for k in db:
    subgroup = db[k,'subgroup']
    if subgroup == 'Bai':
        
        # modify tokens
        tks = db[k,'tokens']
        if tks not in ['-','']:
            tks = tks.split(' ')
            ntk = []
            while tks:
                tk = tks.pop(0)
                if tk[0] in numbersdown:
                    for a,b in zip(numbersdown,numbersup):
                        tk = tk.replace(a,b)
                    ntk += [tk]
                # expand nasals
                elif "\u0303" in tk or tk[0] in "ãũẽĩõ":
                    ntk += [tk,lingpy.rc('nasal_placeholder')]
                else:
                    ntk += [tk]
                    
            db[k][db.header['tokens']] = ' '.join(ntk)

        # same for ipa
        ipa = db[k,'ipa']
        for a,b in zip(numbersdown, numbersup):
            ipa.replace(a,b)
        db[k][db.header['ipa']] = ipa

db._clean_cache()
# assemble cognate ids and align them again for bai
alms = {}
etd = db.get_etymdict(ref='cogid')
for k in etd:
    print ("Carrying out alignment for {0}".format(k))
    idxs = [idx[0] for idx in etd[k] if idx]
    
    nidxs, alms = [], []
    for idx in idxs:
        alm = db[idx,'tokens']
        sbg = db[idx,'subgroup']
        if alm != '-' and alm and sbg=='Bai':
            nidxs += [idx]
            alms += [alm]
            
    if alms:
        msa = lingpy.Multiple(alms)
        msa.lib_align()
        for idx,alm in zip(nidxs,msa.alm_matrix):
            db[idx][db.header['alignment']] = ' '.join(alm)

cidx = db._rowIdx
ignore = []
for k in db:
    
    c = db[k, 'concept']
    if c == 'to plant (grow)':
        db[k][cidx] = 'to plant'
    elif c == 'lie, rest':
        if db[k,'ipa'] == '-' or db[k,'ipa'] == '':
            ignore += [k]
    elif c == 'to the dream':
        db[k][cidx] = 'the dream'
    elif c == 'to suck':
        if db[k,'ipa'] == '-' or db[k,'ipa'] == '':
            db[k][cidx] = 'to lick'
    elif c == 'to work':
        db[k][cidx] = 'the work'

# search for potential duplicates
dups = {}
for d in db.doculect:
    # get data flat
    idxs = db.get_list(doculect=d, flat=True)
    tks = db.get_list(doculect=d, flat=True, entry='tokens')

    # iterate over all tokens and search for identical words
    dup = {}
    for idx,tk in zip(idxs,tks):
        if tk not in ['-','']:
            try:
                dup[tk] += [idx]
            except KeyError:
                dup[tk] = [idx]
    for k in dup:
        if k not in ['-','']:
            if len(dup[k]) > 1:
                basei = dup[k][0]
                basec = db[basei,'concept']
                base = '{0} ({1})'.format(basei, basec)
                for idx in dup[k][1:]:
                    dups[idx] = base
for k in db:
    if k not in dups:
        dups[k] = ''

    if db[k,'ipa'] == '0':
        db[k][db.header['ipa']] = ''
        db[k][db.header['tokens']] = ''


db.add_entries('duplicates', dups, lambda x: x) 

# add line for duplicates

db.update('sinotibetan',verbose=True, delete=ignore)
