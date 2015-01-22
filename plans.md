Plans for Setting up the DB
===========================

## Mapping of Sources

* Burmish data (collaboration with N. Hill)
* Chinese dialect data (partially digitized but not yet parsed, partially by expert contributors)

## Correcting specific entries

### Representation of Nasals

It may make sense to represent nasal vowels represented by two symbols, one for nasalization, and one for the vowel. This helps matching in Alignments without loosing any information and it has be successfully tested in collaboration with N. Hill on Burmish data. It will also definitely help to align Chinese dialect data and Bai dialect data.

### Correct keys for semantic items

Even if trying to be strict in translation of semantic glosses into the target languages, it is not possible to get everything exactly done, especially in the light of sources which are sloppy regarding the semantics. Furthermore, there are certain glosses which are often ambiguously translated by those who want to compile a "Swadesh-List". If we do not want to loose this data, we need to make clear that in certain semantic items, ambiguities may be expected. This can -- for the beginning -- simpy be done by adding two or more OMEGAWIKI-IDs to the OMEGAWIKI column, thus indicating that two different semantic readings are possible (or even an underspecified reading). Here are cases which definitely need to be changed in this way:

* warm / hot: Sinitic sources usually do not give "warm", but always indicate "hot", furthermore, "warm" is often an explicit compound with a more specified meaning than "warm" in European languages
* child (descendant) / child (young human): not many sources make an explicit distinction here. Furthermore, Swadesh himself switched from "child (young human)" to "child (descendant)".
* nail / claw: It seems to be some practice in many Swadesh lists that scholars translate "claw (nail" with "fingernail", if possible. Swadesh himself terms it "claw (nail)", and Chén (1996) follows by translating this as 爪子. IELex glosses it as "fingernail", following the Wiktionary list. In Chinese dialects and Bai, "fingernail" is often a compound word whose internals structure is sometimes not directly obvious. These words are notoriously difficult to align. 

## Preparing the Code for LingPy

LingPy still doesn't handle all parts of the EDICTOR app well enough. Among the problems, here, are:

* Parsing of alignments containing parts to be ignored (indicated by brackets)
* Code for dumb and strict detection of pairwise sound correspondences in a given set of alignments
* Code for the detection of strictly regular change conditions in proto-reflex pairs (experiments have been carried out, but nothing else so far)
* Adding of new entries in the LexiBase class
  - adding of new doculects
  - adding of new entries (whatever column)
  - adding of new concepts
* Removing of entries in the LexiBase class during update

## Preparing the EDICTOR code

* allow for the indication of column mergers in alignments
* allow for the direct merging of columns in alignments (especially diphtongs)
* representation of strict sound correspondences in the edictor
  - take alignments
  - search for context markers (prosodic strings)
    - if they're missing, add them automatically
  - carry out pairwise search for regularities
  - represent findings in a table from one doculect to all other doculects, similar to the [jCoV](https://rawgit.com/dighl/jcov/master/corrs.html) application.
  
## New Analyses

* Parsimony framework for character mapping of ordered multistates
* Framework for cognate detection including partial cognacy


  

