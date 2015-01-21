from lingpyd import *
wl = Wordlist('bai.tsv')
wl.output('tsv', filename='bai_wf', subset=True, rows=dict(source='== "Wang2006a"'),
        ignore=['json', 'msa'])
wl.output('tsv', filename='bai_al', subset=True, 
        rows=dict(source='== "Allen2007"'),
        ignore=['json', 'msa'])

etd = wl.get_etymdict(ref='concept')
concepts = []
for k in etd:
    idxs = [x[0] for x in etd[k] if x]
    sources = [wl[x,'source'] for x in idxs]
    if len(set(sources)) == 2:
        concepts += [k]

    

wl.output('tsv', filename='bai_coverage', subset=True, 
        rows=dict(concept = 'in '+str(concepts)),
        cols=[h for h in wl.header if h not in 
            ['cogid', 'alignment','tokens']])


