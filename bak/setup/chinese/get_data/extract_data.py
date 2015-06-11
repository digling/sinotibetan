# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-10 16:56
# modified : 2015-03-10 16:56
"""
Extract tabular data from cihui.
"""

__author__="Johann-Mattis List"
__date__="2015-03-10"

import re
from lingpyd import *

data = open('beijing-daxue-1964-fangyan-cihui.html').read()
conc = csv2list('BeijingDaxue1964-concepts.csv')

cd = dict([(a[2],a[1]) for a in conc[1:]])

tables = re.findall('<table [^>]*>.*?</table>',data,re.DOTALL)
tables = [t for t in tables if 'width="' in t and '詞目' in t]

idx = 1
f = open('test.txt','w')
glosses = []
for i,table in enumerate(tables):

    trs = re.findall('<tr [^>]*>(.*?)</tr>',table, re.DOTALL)
    
    #for tr in trs[:2]:
    # get the first from trs
    tds = re.findall('<td [^>]*>(.*?)</td>',trs[0], re.DOTALL)
    
    glossA = ''.join(re.findall('<span lang="zh-CN">(.*?)</span>', tds[1]))
    txtA = ''.join(re.findall('<span lang="en-US">(.*?)</span>', tds[1]))
    glossB = ''.join(re.findall('<span lang="zh-CN">(.*?)</span>', tds[2]))
    txtB = ''.join(re.findall('<span lang="en-US">(.*?)</span>', tds[2]))

    glossAX = re.sub('</*b*>','',glossA)
    glossBX = re.sub('</*b>','',glossB)
    txtAX = re.sub('</*b>','',txtA)
    txtBX = re.sub('</*b>', '', txtB)
    
    if glossAX != glossA:
        print(idx,glossAX, glossA)
    else:
        print(idx, glossA, txtAX)
    print(idx+1,glossBX)

    f.write('{0}\t{1}\t{4}\n{2}\t{3}\t{5}\n'.format(
        idx,''.join(glossAX),idx+1,''.join(glossBX),
        txtAX+'\t'+txtA, txtBX+'\t'+txtB))
    print('')
    idx += 2
    
    glosses += [glossAX,glossBX]

print('---')
idx = 1
for g in cd:
    if g not in glosses:
        print(idx, g, '\t',cd[g])
        idx += 1
f.close()
