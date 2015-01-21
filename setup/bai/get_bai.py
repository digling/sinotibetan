from lingpyd import *
from lingpy.convert.plot import *

lex = LexStat('bai_subset.tsv', check=True, merge_vowels=False)
lex.cluster(method='sca', threshold=0.3)
lex.calculate('tree',ref='scaid')
plot_tree(lex.tree)
lex.calculate('groups',threshold=0.2)
lex.output('groups')

alm = Alignments(lex, ref='scaid')
alm.align(method='library')
alm.output('separated',
        filename='bai_data',entries=['omegawiki','ipa','tokens','scaid','source','gloss_in_source','entry_in_source','alignment'],
        ignore_keys = True)

