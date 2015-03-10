# sinotibetan
## Lexical homology database for Sino-Tibetan languages

This is the attempt to create a lexical homology database for Sino-Tibetan languages which wil be subsequently populated with etymologically related lexical entries of various Sino-Tibetan languages. Other databases, like the lexical database of Chinese dialects will be compiled as subparts of this database (partially with additional lexical entries, depending on the amount of data available). 
For the beginning, we have chosen a set of approximately 240 meanings and we started to contribute translations for these meanings in approximately 40 Sino-Tibetan doculects. 
Note that the selection of meanings does not directly reflect any previously published "Swadesh List", but rather a merger of two basic lists, namely the list used in the [ABVD project](http://concepticon.github.io/compare.html?conceptlist=Blust-2008-210), and the list used in the [IELex](http://concepticon.github.io/compare.html?conceptlist=Dunn-2012-207). We were further forced to discard several semantic items which are hard to translate into the respective doculects.
As the datacollection proceeds, we may add further entries, but we hope that the current collection is sufficient as a start and a "proof of concept". 
All lexical entries will be given in plain IPA, in a segmentized form (sound and morpheme segmentation), and all cognate entries will be aligned.

## Database Backend

If you want to browse the current state of the data, you can do this via its [EDICTOR backend](http://tsv.lingpy.org?remote_dbase=sinotibetan.sqlite3&file=sinotibetan&columns=DOCULECT,CONCEPT,IPA,TOKENS,ALIGNMENT,COGID,COMMENT).
If you want to search for specific subsets of the data, you can use our [online tool](http://dighl.github.io/sinotibetan) which creates a specific URL to browse the EDICTOR.

## Overview over Data Collections

Our procedure for data-collection is "multilateral".

* we take existing collections of tabular (wordlist-like) data and map them to our concept list which we partially digitize ourselves, partially take from already digitized sources, like, for example, STEDT
* we take language varieties of specific interest and have them provided either by contributors who did fieldwork on the varieties, or have them extracted manually from written and mostly recent sources

So far, the following collections have already been added to the database:

* Bai languages, taken from two sources (Wang 2006 and Allen 2007), a total of 17 varieties
* Burmish languages from the STEDT project, in collaboration with SOAS, a total of about 10 varieties
* Chinese dialects taken from the Cihui, a large collection published in 1964, covering 17 varieties (in preparation), and further dialect varieties which will be added on a one-source basis
* Data for 50 Tibeto-Burman languages taken from Huang and Dai (1992), already digitized by the [STEDT](https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/source/TBL) project (in preparation)

Apart from these larger collections, we will explicitly add additional Sino-Tibetan languages which are of greater interest for us.
