from pystdb import *
from lingpy.compare.util import mutual_coverage_check
from lingpy import *

wl = load_sinotibetan(remote=False, tsv=True)

etd = wl.get_etymdict(ref='cogid')
concepts = {}
out = [['CONCEPT', 'OCCURRENCE', 'COVERAGE', 'STABILITY', 'COLEXIFICATIONS',
    'COLEXIFICATION_INDEX', 'EXCLUDE']]
for concept in wl.rows:
    concepts[concept] = {}

    # compute concept coverage
    cov = len(set([x for x, y in wl.get_dict(row=concept,
        entry='doculect').items() if y]))
    concepts[concept]['coverage'] = cov / wl.width
    concepts[concept]['occurrence'] = cov

    # compute etymological diversity
    cogids = wl.get_list(row=concept, entry='cogid', flat=True)
    etm = len(set([c for c in cogids if c != 0])) / len(cogids)
    concepts[concept]['stability'] = etm

    # entries
    entries = wl.get_dict(row=concept)
    
    # compute colexification
    colex = []
    summeds = []
    for t in wl.cols:
        these_words = entries.get(t, [])
        all_words = wl.get_list(col=t, entry='tokens', flat=True)
        count, summed = 0, 0
        for w in these_words:
            tks = wl[w, 'tokens']
            for w2 in all_words:
                if tuple(tks) == tuple(w2):
                    count += 1
                summed += 1
        if summed:
            colex += [count]
            summeds += [summed]
    concepts[concept]['colexification'] = sum(colex)
    concepts[concept]['colexification_index'] = sum(colex) / sum(summeds)
    
    print(concept, '{occurrence}\t{stability:.2f}\t{colexification_index:.4f}'.format(**concepts[concept]))

    out += [[concept]+[concepts[concept][x] for x in ['occurrence', 'coverage',
        'stability', 'colexification', 'colexification_index']]]
with open('concepts-ranked.tsv', 'w') as f:
    f.write('\t'.join(out[0])+'\n')
    for line in sorted(out[1:], key=lambda x: (x[2], x[3], 1-x[5]),
            reverse=True):
        f.write('{0[0]}\t{0[1]}\t{0[2]:.2f}\t{0[3]:.2f}\t{0[4]}\t{0[5]:.4f}\t0\n'.format(
            line))
