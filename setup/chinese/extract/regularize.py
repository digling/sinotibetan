# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-02-01 10:32
# modified : 2015-02-01 10:32
"""
Regularize the concepts.
"""

__author__="Johann-Mattis List"
__date__="2015-02-01"

from lingpyd import *
from lingpyd.plugins.chinese import chinese
import urllib
import re
import time
from socket import timeout

lst = csv2list('concepts-bjdx64.csv', strip_lines=False)
cst = csv2list('fields.tsv')

cstD = dict([(c,(a,b)) for a,b,c in cst])

field = ''
pos = ''
out_list = []
sofar = dict([(line[1],line[-1]) for line in csv2list('bjdxc.tsv',
    strip_lines=False) if line[-1] != '?'])

for i,line in enumerate(lst):
    print ('['+str(i+1)+'] Analyzing concept {0}...'.format(line[1]))
    if line[3].strip():
        field = line[3].strip()
    if line[4].strip():
        pos = line[4].strip()

    num = line[0]
    gls = line[1]
    pgn = line[2]
    cls,fld = cstD[field]

    # try to find translation via url
    if gls not in sofar:
        url = 'http://www.zdic.net/sousuo/?q='+urllib.parse.quote(chinese.long2short(gls))
        try:
            req = urllib.request.urlopen(url, timeout=30)
            html = req.read()
            html = str(html, 'utf-8')
            print('... received the html')

            if len(gls) > 1:
                translations = re.findall(
                        '<p class="zdct[0-9]">([^<]*?)<span class="diczx4">\[([^<]*)\]</span>([^<]*?)</p>', 
                        html
                        )
                if translations:
                    tstrings = []
                    for a,b,c in translations:
                        tstrings += ['{0}'.format(
                            #a.replace('(','').replace(')',''),
                            b,
                            #c.replace('∶','')
                            )]
                    tstring = ' // '.join(tstrings)
                    print('... great, I found «{1}» as a translation for «{0}»!'.format(gls, tstring))
                else:
                    tstring = ''
            else:
                translations = re.findall(
                        '<h3>English</h3>.*?<hr class="dichr" />([^<]*)',
                        html
                        )
                if translations:
                    tstring = ' // '.join(translations)
                    print('... found «{0}» as a translation for «{1}»!'.format(tstring,
                        gls))
                else:
                    tstring = ''
            
            time.sleep(5)
        except:
            print ("timeout, skipping this")
            tstring = '?'

    else:
        tstring = sofar[gls]

    with open('bjdxc.tsv', 'a') as mf:
        mf.write('\t'.join([num,gls,pgn,cls,fld,field,pos,tstring])+'\n')

    out_list += [(num,gls,pgn,cls,fld,field,pos,tstring)]



with open('BejingDaxue1964-concepts.tsv', 'w') as f:
    f.write('NUMBER\tCHINESE_GLOSS\tPAGENO\tPOS\tSEMANTIC_FIELD\tSF_IN_SOURCE\tPOS_IN_SOURCE\n')
    for line in out_list:
        f.write('\t'.join(line)+'\n')

        
    

