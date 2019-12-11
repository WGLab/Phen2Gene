# Phen2Gene

Phen2Gene is a phenotype-driven gene prioritization tool, that takes HPO (Human Phenotype Ontology) IDs as inputs, searches and prioritizes candidate causal disease genes.  It is distributed under [the MIT License by Wang Genomics Lab](https://wglab.mit-license.org/).  Additionally we have provided a [web server](https://phen2gene.wglab.org) and an associated RESTful API service for running Phen2Gene.  Finally, a mobile app for Phen2Gene and several other genetic diagnostic tools from our lab is being tested and will be available soon.

## Prerequisites

If you do not wish to use Anaconda, simply install the packages in the file `environment.yml` using `pip`.

## Installation
First, install Miniconda, a minimal installation of Anaconda, which is much smaller and has a faster installation.
Note that this version is meant for Linux below, macOS and Windows have a different script:

```
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Go through all the prompts (installation in `$HOME` is recommended).
After Anaconda is installed successfully, simply run:

```
git clone https://github.com/WGLab/Phen2Gene.git
cd Phen2Gene
conda env create -f environment.yml
conda activate phen2gene
bash getKB.sh
```

## General Use Case

This software can be used in one of three scenarios:

1. Ideally, you have a list of physician-curated HPO terms describing a patient phenotype and a list of potential candidate disease variants that overlap gene space and you want to narrow down the list of variants by prioritizing candidate disease genes, often in tandem with variant prioritization software, which cannot as of yet score STR expansions or SVs unlike Phen2Gene which is variant agnostic.
2. You do not have variants, but you have HPO terms and would like to get some candidate genes for your disease that you may want to target sequence, as it is much cheaper than whole-genome or whole-exome sequencing.
3. If you have clinical notes, you can use tools like [EHR-Phenolyzer](https://github.com/WGLab/EHR-Phenolyzer) or [Doc2HPO](https://impact2.dbmi.columbia.edu/doc2hpo/) for processing clinical notes into HPO terms using natural language processing (NLP) techniques, then apply scenario 1 or 2 as relevant.


### Input files
Input files to Phen2Gene should contain HPO IDs, separated by UNIX-recognized new line characters (i.e., `\n`).
Alternatively you can use a space separated list of HPO IDs on the command line.

### Examples of how to run Phen2Gene with the `provided HPO_sample.txt` file

1. Input HPO IDs via input file (typical use case)
```
python phen2gene.py -f example/HPO_sample.txt -out out/prioritizedgenelist
```
2. Use Skewness and Information Content

  * `-w sk` uses a skewness-based weighting of genes for each HPO term (default, and recommended)
  * `-w w` and `-w ic` do not use skew, but utilize information content in the tree structure (slightly worse performance)
  * `-w u` is unweighted

```
python phen2gene.py -f example/HPO_sample.txt -w sk -out out/prioritizedgenelist
```
3. Run Phen2Gene with verbose messages
```
python phen2gene.py -f example/HPO_sample.txt -v -out out/prioritizedgenelist
```
4. Input HPO IDs manually, if desired
```
python phen2gene.py -m HP:0000021 HP:0000027 HP:0030905 HP:0010628 -out out/prioritizedgenelist
```

## RESTful API and Web Server

Examples of how to use the [Web Server](https://phen2gene.wglab.org/) and the RESTful API can be found in the [Docs](https://phen2gene.wglab.org/docs).

## Getting Help

Please use the [Phen2Gene issues page](https://github.com/WGLab/Phen2Gene/issues) if you have any questions!

## Creating the benchmark data figures from the manuscript

In order, run:
```
bash getKB.sh
```
```
bash getbenchmark.sh
```
```
bash runtest.sh
```

The figures are in the folder `figures`.

## Example of Use Case #2, where you have filtered candidate variants (also in the manuscript)

After changing the code `example/ANKRD11example.sh` so the ANNOVAR db is built where you would like it, simply run:

```
bash example/ANKRD11example.sh
```

Going through the code in `example/ANKRD11example.sh`, first one downloads a list of candidate variants from the article referenced in the manuscript where the patient has KBG syndrome.

Then, we annotate with ANNOVAR to retrieve gene annotations for these variants, functional consequence information (exonic, intronic, nonsynonymous), amino acid change information, and population frequency.

We next filter out common variants (>1% in gnomAD 2.1.1) and use Phen2Gene to rank the candidate genes based on HPO terms.

Combining this information with the variants, we can re-rank Phen2Gene's candidate list as in the script `filterbyannovar.py` and discover that the variant for the causal gene _ANKRD11_ is now ranked number 1 after being ranked number 2 by HPO term.  The number 1 ranked gene by HPO, _VPS13B_, is filtered out because the only candidate variant (8-100133706-T-G) has an extremely high allele frequency in gnomAD(74%!).
