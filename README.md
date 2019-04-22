# Phen2Gene
Phenotype driven gene prioritization tool. 

Phen2Gene reads HPO terms, and output a prioritized candidate gene list.

# Requirments
1. Python3 and numpy

2. Linux environments recommended

# Test

Input by file
```
python phen2gene.py -f sample.txt -v
```

Input by HPO terms
```
python phen2gene.py -m HP:0002779 HP:0001631 HP:0030718 HP:0005117 HP:0001156 HP:0000426 HP:0000316 -v
```

Use weighted human phenotype terms for scoring
```
python phen2gene.py -f sample.txt -w w -v
```

Use unweighted human phenotype terms for scoring
```
python phen2gene.py -f sample.txt -w u -v
```

# Usage

```

python phen2gene.py [-h] [-f [FILE.NAME [FILE.NAME ...]]]

             [-m [HPID [HPID ...]]] [-w w|u] [-v] [-out OUTPUT]
             
optional arguments:

  -h, --help            show this help message and exit
  
  -f [FILE.NAME [FILE.NAME ...]], --file [FILE.NAME [FILE.NAME ...]]

                        Input HPO as file.
  -m [HPID [HPID ...]], --manual [HPID [HPID ...]]
                        Input HPO ID(s) one by one, seperated by an empty
                        space.
  -w w|u, --method w|u  Methods to merge gene scores. 
                        'w' ( Default ) Scoring by weighted Human-Phenotype terms.
                        'u' Scoring by Unweighted Human-Phenotype terms.
  -v, --verbosity       Display Phen2Gene workflow verbosely.
  -out OUTPUT, --output OUTPUT
                        Specify the path to store output files. Default
                        directory path: ./out/
```
