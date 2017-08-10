from lingpy import *
from lingpy.compare.partial import Partial
from collections import defaultdict
import networkx as nx
from lingpy.sequence.sound_classes import get_all_ngrams
from networkx.algorithms.bipartite.projection import weighted_projected_graph

def consensus_matrix(wl, concept, ref):
    idxs = wl.get_list(row=concept, flat=True)
    cogids = [wl[idx, ref] for idx in idxs]
    
    #partitions = set()
    #for cogs in cogids:
    #    for pt in get_all_ngrams(cogs):
    #        partitions.add(' '.join([str(x) for x in pt]))
    #
    #for 
    allcogs = set()
    for cogs in cogids:
        for c in cogs:
            allcogs.add(c)
    G = nx.Graph()
    for i, cogs in enumerate(cogids):
        G.add_node(idxs[i], ntype=1)
        for c in cogs:
            G.add_edge(idxs[i], str(c))

    G2 = weighted_projected_graph(G, idxs)
    edge_weights = [d['weight'] for _, _, d in G2.edges(data=True)]
    medgew = max(edge_weights)
    for e1, e2, d in G2.edges(data=True):
        if d['weight'] < medgew / 2:
            G2.remove_edge(e1, e2)
    tmp = {}
    for i, cm in enumerate(nx.connected_components(G2)):
        for c in cm:
            tmp[c] = i+1
    return tmp

def no_partial_cognates(wl, concept, ref):
    idxs = wl.get_list(row=concept, flat=True)
    cogids = [wl[idx, ref] for idx in idxs]
    G = nx.Graph()
    for idx, cogs in zip(idxs, cogids):
        pass


if __name__ == '__main__':
    wl = Wordlist('d_bed.tsv')
    for c in wl.rows:
        tmp = consensus_matrix(wl, c, 'cogids')
        idxs = wl.get_list(row=c, flat=True)
        words = wl.get_list(row=c, flat=True, entry='ipa')
        cogids = wl.get_list(row=c, flat=True, entry='cogids')
        for idx, cogid, ipa in zip(idxs, cogids, words):
            print(c, '\t', idx, '\t', tmp[idx], '\t', ipa, '\t', ' '.join([str(x) for x in
                cogid]))
