# Procedure for synchronizing data from STEDT with our STDB

We will initially concentrate on the large sources in STEDT, containing some more than 20 languages and basically tabular data. This is for practical reasons (it is less work to map all the meanings to basic vocabulary range), but also for consistency reasons (one source for multiple languages turns to be more similar regarding the transcription, and it is also easier for researchers to go back to the respective source). 
These sources are labelled as "Synonym set" in STEDT and a full list of available sources in this format can be retrieved by searching for [Synonym Sets](https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/edit/srcbib?srcbib.format=Synonym%20Sets) in STEDT.

So far, it seems that the following sources should serve as our basic target:

* [TBL](https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/source/TBL), containing some 50 languages from various branches with about 1700 entries (concept glosses) each.
* [ZMYYC](https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/source/ZMYYC), containing 52 language from various branches with about 1000 entries (concept glosses) each, and possibly
* [GEM-CNL](https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/source/GEM-CNL), containing 40 languages on various branches, mostly from the Naga-group.

STEDT offers all those sources for download, but download doesn't contain STEDT's additional markup, like annotation according to synonym sets (although this is rather coarse), or annotation regarding cognacy (although this is rather sparse). Nevertheless, this information is also important for us, especially also as a reference point, which is why we write an url-parser for each entry-id in STEDT to retrieve the relevant annotation.

# Steps for data preparation

In order to prepare the data, we follow the following steps:

* conversion to LingPy-Wordlist format (this requires smaller edits to the STEDT csv-files, but is basically identical with STEDT's format)
* checking which languages from which source we want to include (we should, if possible, only take one source per language, and keep multiple sources for those cases where we do not have sufficient data)
* extraction of glosses (glosses are all in English in STEDT, but glosses in the original data are often in Chinese, so we probably should consider checking the Chinese glosses for the most important words)
* mapping of glosses to the Concepticon (this may turn out to be tedious, but we can restrict our initial search to subsets, like the one we want to have in our database)
* cleaning lexical entries from Entry-In-Source to IPA and to TOKENS (computational process with additional manual cleaning required)
* searching for STEDT annotations with crawling software on a per-entry basis

Once these steps have been undertaken, we can start with cognate judgments and the like. Here, we can, provided we have larger datasets, start to use LingPy's automatic methods for cognate detection (probably enhanced by search containing morphological annotations).

# Overlap between the three sources

The overlap between the sources is not very large. Of a total of 121 
language varieties distinguished in STEDT, only 14 occur in 2 sources and only 3 occur in all three sources:


| Language Name      | Number of Sources | Sources           |
|--------------------|-------------------|-------------------|
| Achang (Longchuan) | 2                 | zmyyc/tbl         |
| Atsi [Zaiwa]       | 2                 | zmyyc/tbl         |
| Bai (Jianchuan)    | 2                 | zmyyc/tbl         |
| Darang [Taraon]    | 2                 | zmyyc/tbl         |
| Guiqiong           | 2                 | zmyyc/tbl         |
| Jinuo              | 2                 | zmyyc/tbl         |
| Kaman [Miju]       | 2                 | zmyyc/tbl         |
| Lisu               | 2                 | zmyyc/tbl         |
| Namuyi             | 2                 | zmyyc/tbl         |
| Qiang (Mawo)       | 2                 | zmyyc/tbl         |
| Tibetan (Lhasa)    | 2                 | zmyyc/tbl         |
| Tujia              | 2                 | zmyyc/tbl         |
| Xumi               | 2                 | zmyyc/tbl         |
| Yi (Nanhua)        | 2                 | zmyyc/tbl         |
| Yi (Xide)          | 2                 | zmyyc/tbl         |
| Burmese (Written)  | 3                 | gem-cnl/zmyyc/tbl |
| Jingpho            | 3                 | gem-cnl/zmyyc/tbl |
| Tibetan (Written)  | 3                 | gem-cnl/zmyyc/tbl |

This means, that we can largely work independently with all three sources, and see how far we get with them. Given that the amount of semantic glosses is rather large in all three sources, we can hope to get a very good coverage for all the data.

Here's the list of all doculects in the three sources:

| NO  | Language Name            | Number of Sources | Source            |
|-----|--------------------------|-------------------|-------------------|
| 1   | Achang (Xiandao)         | 1                 | tbl               |
| 2   | Angami (Khonoma)         | 1                 | gem-cnl           |
| 3   | Angami (Kohima)          | 1                 | gem-cnl           |
| 4   | Anong                    | 1                 | zmyyc             |
| 5   | Ao (Chungli)             | 1                 | gem-cnl           |
| 6   | Ao (Mongsen: Longchang)  | 1                 | gem-cnl           |
| 7   | Bai (Bijiang)            | 1                 | zmyyc             |
| 8   | Bai (Dali)               | 1                 | zmyyc             |
| 9   | Bokar                    | 1                 | tbl               |
| 10  | Bokar Lhoba              | 1                 | zmyyc             |
| 11  | Bola (Luxi)              | 1                 | tbl               |
| 12  | Burmese (Rangoon)        | 1                 | tbl               |
| 13  | Burmese (Spoken Rangoon) | 1                 | zmyyc             |
| 14  | Chang                    | 1                 | gem-cnl           |
| 15  | Chokri                   | 1                 | gem-cnl           |
| 16  | Cuona Menba              | 1                 | tbl               |
| 17  | Daofu                    | 1                 | tbl               |
| 18  | Dimasa                   | 1                 | gem-cnl           |
| 19  | Dulong                   | 1                 | tbl               |
| 20  | Ergong (Danba)           | 1                 | zmyyc             |
| 21  | Ersu                     | 1                 | zmyyc             |
| 22  | Gazhuo                   | 1                 | tbl               |
| 23  | Hani (Caiyuan)           | 1                 | zmyyc             |
| 24  | Hani (Dazhai)            | 1                 | zmyyc             |
| 25  | Hani (Lüchun)            | 1                 | tbl               |
| 26  | Hani (Mojiang)           | 1                 | tbl               |
| 27  | Hani (Shuikui)           | 1                 | zmyyc             |
| 28  | Idu                      | 1                 | zmyyc             |
| 29  | Karen                    | 1                 | tbl               |
| 30  | Khezha                   | 1                 | gem-cnl           |
| 31  | Khoirao                  | 1                 | gem-cnl           |
| 32  | Konyak                   | 1                 | gem-cnl           |
| 33  | Lahu (Black)             | 1                 | zmyyc             |
| 34  | Lahu (Lancang)           | 1                 | tbl               |
| 35  | Langsu (Luxi)            | 1                 | tbl               |
| 36  | Leqi (Luxi)              | 1                 | tbl               |
| 37  | Liangmei                 | 1                 | gem-cnl           |
| 38  | Lotha Naga               | 1                 | gem-cnl           |
| 39  | Lushai [Mizo]            | 1                 | gem-cnl           |
| 40  | Lyuzu                    | 1                 | tbl               |
| 41  | Mao                      | 1                 | gem-cnl           |
| 42  | Maram                    | 1                 | gem-cnl           |
| 43  | Maring                   | 1                 | gem-cnl           |
| 44  | Maru [Langsu]            | 1                 | zmyyc             |
| 45  | Meithei                  | 1                 | gem-cnl           |
| 46  | Meluri                   | 1                 | gem-cnl           |
| 47  | Mikir [Karbi]            | 1                 | gem-cnl           |
| 48  | Motuo Menba              | 1                 | tbl               |
| 49  | Muya                     | 1                 | tbl               |
| 50  | Muya [Minyak]            | 1                 | zmyyc             |
| 51  | Mzieme                   | 1                 | gem-cnl           |
| 52  | Naxi                     | 1                 | tbl               |
| 53  | Naxi (Lijiang)           | 1                 | zmyyc             |
| 54  | Naxi (Yongning)          | 1                 | zmyyc             |
| 55  | Nocte                    | 1                 | gem-cnl           |
| 56  | Ntenyi                   | 1                 | gem-cnl           |
| 57  | Nung                     | 1                 | tbl               |
| 58  | Nusu (Bijiang)           | 1                 | zmyyc             |
| 59  | Nusu (Central)           | 1                 | tbl               |
| 60  | Phom                     | 1                 | gem-cnl           |
| 61  | Puiron                   | 1                 | gem-cnl           |
| 62  | Pumi (Jiulong)           | 1                 | tbl               |
| 63  | Pumi (Lanping)           | 1                 | tbl               |
| 64  | Pumi (Qinghua)           | 1                 | zmyyc             |
| 65  | Pumi (Taoba)             | 1                 | zmyyc             |
| 66  | Qiang (Taoping)          | 1                 | zmyyc             |
| 67  | Queyu (Xinlong)          | 1                 | tbl               |
| 68  | Queyu (Yajiang) [Zhaba]  | 1                 | zmyyc             |
| 69  | Rengma                   | 1                 | gem-cnl           |
| 70  | Rongmei / Nruanghmei     | 1                 | gem-cnl           |
| 71  | Sangtam                  | 1                 | gem-cnl           |
| 72  | Sema [Sumi]              | 1                 | gem-cnl           |
| 73  | Sulung [Puroik]          | 1                 | zmyyc             |
| 74  | Tangkhul                 | 1                 | gem-cnl           |
| 75  | Tangsa (Moshang)         | 1                 | gem-cnl           |
| 76  | Tangsa (Yogli)           | 1                 | gem-cnl           |
| 77  | Tangut [Xixia]           | 1                 | zmyyc             |
| 78  | Tengsa                   | 1                 | gem-cnl           |
| 79  | Tibetan (Alike)          | 1                 | tbl               |
| 80  | Tibetan (Amdo:Bla-brang) | 1                 | zmyyc             |
| 81  | Tibetan (Amdo:Zeku)      | 1                 | zmyyc             |
| 82  | Tibetan (Batang)         | 1                 | tbl               |
| 83  | Tibetan (Khams:Dege)     | 1                 | zmyyc             |
| 84  | Tibetan (Xiahe)          | 1                 | tbl               |
| 85  | Trung [Dulong]           | 1                 | zmyyc             |
| 86  | Tsangla (Motuo)          | 1                 | zmyyc             |
| 87  | Tshona (Mama)            | 1                 | zmyyc             |
| 88  | Wancho                   | 1                 | gem-cnl           |
| 89  | Yacham                   | 1                 | gem-cnl           |
| 90  | Yacham-Tengsa            | 1                 | gem-cnl           |
| 91  | Yi (Dafang)              | 1                 | zmyyc             |
| 92  | Yi (Mile)                | 1                 | zmyyc             |
| 93  | Yi (Mojiang)             | 1                 | zmyyc             |
| 94  | Yi (Nanjian)             | 1                 | zmyyc             |
| 95  | Yi (Sani)                | 1                 | tbl               |
| 96  | Yi (Weishan)             | 1                 | tbl               |
| 97  | Yi (Wuding)              | 1                 | tbl               |
| 98  | Yidu                     | 1                 | tbl               |
| 99  | Yimchungrü               | 1                 | gem-cnl           |
| 100 | Zeme                     | 1                 | gem-cnl           |
| 101 | Zhaba (Daofu County)     | 1                 | tbl               |
| 102 | rGyalrong                | 1                 | zmyyc             |
| 103 | rGyalrong (Maerkang)     | 1                 | tbl               |
| 104 | Achang (Longchuan)       | 2                 | zmyyc/tbl         |
| 105 | Atsi [Zaiwa]             | 2                 | zmyyc/tbl         |
| 106 | Bai (Jianchuan)          | 2                 | zmyyc/tbl         |
| 107 | Darang [Taraon]          | 2                 | zmyyc/tbl         |
| 108 | Guiqiong                 | 2                 | zmyyc/tbl         |
| 109 | Jinuo                    | 2                 | zmyyc/tbl         |
| 110 | Kaman [Miju]             | 2                 | zmyyc/tbl         |
| 111 | Lisu                     | 2                 | zmyyc/tbl         |
| 112 | Namuyi                   | 2                 | zmyyc/tbl         |
| 113 | Qiang (Mawo)             | 2                 | zmyyc/tbl         |
| 114 | Tibetan (Lhasa)          | 2                 | zmyyc/tbl         |
| 115 | Tujia                    | 2                 | zmyyc/tbl         |
| 116 | Xumi                     | 2                 | zmyyc/tbl         |
| 117 | Yi (Nanhua)              | 2                 | zmyyc/tbl         |
| 118 | Yi (Xide)                | 2                 | zmyyc/tbl         |
| 119 | Burmese (Written)        | 3                 | gem-cnl/zmyyc/tbl |
| 120 | Jingpho                  | 3                 | gem-cnl/zmyyc/tbl |
| 121 | Tibetan (Written)        | 3                 | gem-cnl/zmyyc/tbl |


