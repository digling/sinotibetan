# Basic folder containing the data in CSV files and JSON

Here, I assemble a couple of scripts to work with the data. 

* helper-xxx.py scripts are dated and used to temporarily change certaint things, they are not to be used recurrently and serve most of the time a single purpose (like correction and the like). They take either the most recent Wordlist of the data or the sqlite3-dbase itself as input
* webapp.py creates the web application which allows the user to browse and edit the data interactively, using the EDICTOR tool
* coverage.py creates a current coverage dump of the data, which compares those concepts in the data which we deem as the most important (most "basic") ones (currently 249 concepts, don't ask, how this number could be set up...)

More scripts will probably come. I also store backups of the data in the bak-folders, including dumps of sqlite3, but also of the wordlist-format (equivalent to sqlite3, but without change-tracking).
