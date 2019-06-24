# Phen2Gene

Phen2Gene is a phenotype driven gene prioritization tool, that takes HPO(Human Phenotype Ontology) ID(s) as inputs, searches and prioritize suspected genes.

## Prerequisite
```
Python 3.7
Numpy
```

## Installation
### Python 3.7
Here shows installing Python 3.7 by `Anaconda` (Anaconda installation instruction: https://docs.anaconda.com/anaconda/install/). Usually Python 3.7 is installed at the same time Anaconda is installed.
If you want to run Python 3 under different environment, you may create a new environment for Python 3 in commandline by `conda create -n <environment name> python=3.7`, then `conda activate <environment name>` (on Linux/Mac).

To exit the environment, `source deactivate`.

### Numpy
Here shows installing in commandline by `Anaconda`: `conda install numpy`.

### Phen2Gene
`git clone https://github.com/WGLab/Phen2Gene.git`

### Install Time
It may take a few minutes to install Phen2Gene.

### After Installation
`cd YOUR/PATH/TO/PHEN2GENE`

## Usage
```
usage: phen2gene.py [-h] [-f [FILE.NAME [FILE.NAME ...]]]
                    [-ud [TERM&WEIGHT [TERM&WEIGHT ...]]]
                    [-m [HPID [HPID ...]]] [-w w|u|s|ic|d] [-v] [-wo]
                    [-out OUTPUT] [-n output.file.name]

Phen2Gene: Phenotype driven gene prioritization tool. Phen2Gene take input
data (HPO, Human Phenotype Ontology), and output a prioritized suspected gene
list.

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE.NAME [FILE.NAME ...]], --file [FILE.NAME [FILE.NAME ...]]
                        Input file(s) of HP IDs.
  -ud [TERM&WEIGHT [TERM&WEIGHT ...]], --user_defined [TERM&WEIGHT [TERM&WEIGHT ...]]
                        Input file(s) of HP IDs and user-defined weights.
  -m [HPID [HPID ...]], --manual [HPID [HPID ...]]
                        Input HPO ID(s) one by one, seperated by an empty
                        space.
  -w w|u|s|ic|d, --weight_model w|u|s|ic|d
                        Methods to merge gene scores. 'w' ( Default ) Scoring
                        by weighted Human-Phenotype terms 'u' Scoring by
                        Unweighted Human-Phenotype terms
  -v, --verbosity       Display Phen2Gene workflow verbosely.
  -wo, --weight_only    Output weights of HPO terms only.
  -out OUTPUT, --output OUTPUT
                        Specify the path to store output files. Default
                        directory path: ./out/
  -n output.file.name, --name output.file.name
                        Name the output file.


```

## Input files
Input files to Phen2Gene should contains only HPO ID(s), seperated by new line character(`\n`).

## Example
1. Input HPO ID(s) manually
```
python phen2gene.py -m HP:0000001 HP:0000021 HP:0000027 HP:0030905 HP:0030910 HP:0010628 -out out/out
```
2. Input HPO ID(s) by files
```
python phen2gene.py -f sample.txt -out out/out
```
3. Use Weighted Score Merge
```
python phen2gene.py -f sample.txt -w w -out out/out
```
4. Run Phen2gene verbosely
```
python phen2gene.py -f sample.txt -v -out out/out
```


## Getting Help

Please use the [GitHub's Issues page](https://github.com/WGLab/LinkedSV/issues) if you have questions.


