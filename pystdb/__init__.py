from clldutils.dsv import UnicodeReader
from clldutils.misc import slug
import os
from pyconcepticon.api import Concepticon
from functools import partial
from lingpy._plugins.lpserver.lexibase import LexiBase
from lingpy import *
from lingpy.convert.strings import write_nexus
from collections import OrderedDict, defaultdict

import zipfile
from urllib import request
import zlib
from .data import url
from .util import *


def load_concepticon():

    concepticon = dict([
        (line.id, line) for line in Concepticon().conceptsets.values()
        ])

    return concepticon

def stdb_path(*comps):
    """
    Our data-path in CLICS.
    """
    return os.path.join(os.path.dirname(__file__), os.pardir, *comps)

def load_sinotibetan(remote=False, tsv=False):
    
    if tsv:
        return Wordlist(stdb_path('dumps', 'sinotibetan.tsv'),
                conf=stdb_path('conf', 'wordlist.rc'))
        
    if not remote:
        db = LexiBase('sinotibetan', dbase=stdb_path('sqlite', 'sinotibetan.sqlite3'))
    else:
        db = LexiBase('sinotibetan', dbase=stdb_path('sqlite',
            'sinotibetan.sqlite3'), 
            url='sinotibetan.sqlite3')
    return db

def stdb_concepts():

    with UnicodeReader(stdb_path('concepts', 'concepts.tsv'), delimiter='\t') as reader:
        data = list(reader)
    concepts = {}
    for line in data[1:]:
        if line[1] in concepts:
            print(line[1])
        concepts[line[1]] = OrderedDict(zip([h.lower() for h in data[0]], line))
    return concepts
    
def backup(target='url'):
    """
    Function downloads dataset in actual version and saves it in zipped folder
    """
    
    time = rc('timestamp')
    if target == 'url':
        with request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with zipfile.ZipFile(stdb_path('dumps', 'bak-'+time+'.zip'), 
                'w',
                compression=zipfile.ZIP_DEFLATED
                ) as zf:
            zf.writestr('sinotibetan.tsv', data)
        

def download(target='url'):
    if target == 'url':
        with request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open(stdb_path('dumps', 'sinotibetan.tsv'), 'w') as f:
            f.write(data)

def history(limit):

    url='http://tsv.lingpy.org/triples/get_data.py?history=true&remote_dbase=sinotibetan.sqlite3&limit={0}'.format(limit)

    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        for line in data.split('\n'):
            print(line)


def concept_coverage():

    concepts = [h['concepticon_id'] for h in stdb_concepts().values()]
    concepticon = Concepticon()
    lists = ['Blust-2008-210', 'Comrie-1977-207', 'Matisoff-1978-200']
    for l in lists:
        cids = [c.concepticon_id for c in concepticon.conceptlists[l].concepts.values()]
        olap = len([x for x in concepts if x in cids])
        print('*', l, olap)

def make_nexus(filename, exclude_borrowings=True, concept_rank=226):

    wl = load_sinotibetan(tsv=True)

    if exclude_borrowings:
        ncog = max([int(wl[k, 'cogid']) for k in wl])+1
        for k in wl:
            if wl[k, 'borrowing'].strip():
                wl[k][wl.header['cogid']] = str(ncog)
                ncog += 1
            elif wl[k, 'cogid'] in ['0', '']:
                wl[k][wl.header['cogid']] = str(ncog)
                ncog += 1

    concepts_ = [k for k, v in stdb_concepts().items() if int(v['rank']) <
            concept_rank]


    cogids = defaultdict(lambda : defaultdict(list))
    cogid2concept = {}
    wl.add_entries('paps', 'concept,cogid', lambda x, y:
            x[y[0]]+':'+x[y[1]])
    uncertainties = defaultdict(list)
    for k, doculect, cogid, concept, borrowing in iter_rows(
            wl, 'doculect', 'paps', 'concept', 'borrowing'):
        if borrowing.strip() and not exclude_borrowings:
            uncertainties[cogid].append(doculect)
        cogids[concept][cogid].append(doculect)
        cogid2concept[cogid] = concept

    blocks = []
    concepts = sorted(cogids)
    characters = {}
    ccount = 1
    cstrings = []
    for concept in [c for c in concepts if c in concepts_]:
        cstring = '_'.join([slug(c) for c in concept.split(' ')])
        blocks += [
                'charset '+cstring+' = '
                ]
        cstrings += [cstring]
        start = ccount
        for cogid in sorted(cogids[concept]):
            characters[cogid] = ccount
            ccount += 1
        blocks[-1] += '{0}-{1};'.format(start, ccount-1)
    matrix = []
    print(len(characters), ccount, len(cstrings))
    for taxon in wl.taxa:
        tcids_ = wl.get_list(doculect=taxon, entry='paps', flat=True)
        tcons_ = wl.get_list(doculect=taxon, entry='concept', flat=True)
        
        # transform data, only take things with the same concept, so we check
        # for each datapoint, whether we find it
        tcids, tcons = [], []
        for a, b in zip(tcids_, tcons_):
            if b in concepts:
                tcids += [a]
                tcons += [b]

        matrix += [[]]
        for cogid, idx in sorted(characters.items(), key=lambda x: x[1]):
            if cogid not in tcids:
                concept = cogid2concept[cogid]
                if concept in tcons:
                    matrix[-1] += ['0']
                else:
                    matrix[-1] += ['?']
            else:
                if taxon in uncertainties[cogid]:
                    matrix[-1] += ['10']
                else:
                    matrix[-1] += ['1']

    partition = 'partition favored = {0}: {1}'.format(
            len(blocks),
            ', '.join(cstrings)+';')
    commands = [
            'set autoclose=yes nowarn=yes;',
            'lset coding=noabsencesites rates=gamma;'
            ] + blocks+[partition] + [
                    'taxset fossils = Old_Chinese Old_Tibetan Old_Burmese;',
                    'constraint root = 1-.;',
                    #'prest clockratepr = normal(1E-5,1);',
                    'calibrate Old_Chinese = uniform(2200, 3000);',
                    'calibrate Old_Tibetan = fixed(1200);',
                    'calibrate Old_Burmese = fixed(800);'
                    ] +[
            #'taxset problematic = Naxi Pumi_Lanping Qiang_Mawo Xumi Lyuzu Bai_Jianchuan Tujia;',
            #'delete problematic;',
            'prset clockratepr=exponential(3e5);',
            'prset treeagepr=uniform(4000,20000);',
            'prset sampleprob=0.2 samplestrat=random speciationpr=exp(1);',
            'prset extinctionpr=beta(1,1) nodeagepr=calibrated;'
            'prset brlenspr=clock:fossilization clockvarpr=igr;',
            'mcmcp ngen=10000000 printfreq=10000 samplefreq=2500 nruns=2 ' 
            'nchains=4 savebrlens=yes filename={0};'.format(filename)]
    print(filename)
    write_nexus(taxa=wl.taxa, matrix=matrix, commands=commands,
            filename=filename+'.nex')

            

