from pystdb import *

def main():
    from sys import argv
    target, limit = 'url', 10
    if '-t' in argv:
        target = argv[argv.index('-t')+1]
    if '-l' in argv:
        limit = int(argv[argv.index('-l')])

    if 'backup' in argv:
        backup(target)
    if 'download' in argv:
        download(target)
    if 'history' in argv:
        history(limit)
    if 'coverage' in argv:
        concept_coverage()

