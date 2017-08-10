from pystdb import *
from pystdb.concepts import *
from pystdb.data import url

def main():
    from sys import argv
    target, limit, taxon, path = 'url', 10, None, None
    if '-t' in argv:
        target = argv[argv.index('-t')+1]
    if '-l' in argv:
        limit = int(argv[argv.index('-l')])
    if '--taxon' in argv:
        taxon = argv[argv.index('--taxon')+1]
    if '-p' in argv:
        path = argv[argv.index('-p')+1]
    if '--concepts' in argv:
        concepts = int(argv[argv.index('--concepts')+1])+1
    else:
        concepts = 227

    if 'backup' in argv:
        backup(target)
    if 'download' in argv:
        download(target)
    if 'history' in argv:
        history(limit)
    if 'coverage' in argv:
        if taxon and path:
            print(taxon, path)
            check_coverage(path, taxon)
        else:
            concept_coverage()
    if 'open' in argv:
        if 'github' in argv:
            os.system('firefox --new-tab https://github.com/digling/sinotibetan')
        elif 'edictor' in argv:
            os.system('firefox --new-tab "{0}"'.format(url.replace('/triples/get_data.py', ''))
                    )
        else:
            os.system('firefox --new-tab https://dighl.github.io/sinotibetan')
    
    if 'nexus' in argv:
        make_nexus(argv[argv.index('nexus')+1], concept_rank=concepts)
        

