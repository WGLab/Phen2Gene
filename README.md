# Phen2Gene
Phen2Gene is a phenotype driven gene prioritization tool, that takes HPO(Human Phenotype Ontology) ID(s) as inputs, searches and prioritize suspected genes.

## Prerequisite
```
Python 3.7
Numpy
```

## Installation
### Python 3.7
Python 3 can be installed by multiple ways. Here shows installing Python 3.7 by `Anaconda` (Anaconda installation instruction: https://docs.anaconda.com/anaconda/install/). Usually Python 3.7 is installed at the same time Anaconda is installed.
If you want to run Python 3 under different environment, you may create a new environment for Python 3 by `conda create -n <environment name> python=3.7`, then `source activate <environment name>` (on Linux/Mac).

To exit the environment, `source deactivate`.

### Numpy
Numpy can be installed by multiple ways after Python is installed. Here shows installing by `Anaconda`: `conda install numpy`.

### Phen2Gene
`git clone https://github.com/WGLab/Phen2Gene.git`

### Install Time
It may take a few minutes to install Phen2Gene.

### After Installation
`cd YOUR/PATH/TO/PHEN2GENE`


## Usage
```
usage: phen2gene.py [-h] [-f [FILE.NAME [FILE.NAME ...]]]
                    [-m [HPID [HPID ...]]] [-w w|s] [-v] [-out OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f, --file [FILE.NAME [FILE.NAME ...]]
                        Input HPO as file.
  -m, --manual [HPID [HPID ...]]
                        Input HPO ID(s) one by one, with an empty space as seperation.
  -w, --method w|s  Methods to merge gene scores. 
                        'w' ( Default ) Weighted Score Merge 
                        's' Simple Score Merge
  -v, --verbosity       Display Phen2Gene workflow verbosely.
  -out, --output OUTPUT/PATH
                        Specify the path to store output files. 
                        Default directory path: ./out/

```

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
