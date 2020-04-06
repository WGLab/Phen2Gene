#!/usr/bin/sh

printf "Calculating p-values....\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/pvalues.zip -O pvalues.zip && unzip -qo pvalues.zip -d testing_data && rm pvalues.zip

python testing_data/pvalue.py -s testing_data/signtest_pvaluesAJHG_CSH.tsv testing_data/signtest_pvaluesTAF1.tsv testing_data/signtest_pvaluesDGD.tsv testing_data/signtest_pvaluesColumbia.tsv -o testing_data/pvalues.tsv -he 'Phen2Gene vs Phenolyzer' 'Phen2Gene vs Amelie' 'Phen2Gene vs GADO'
printf "p-values are stored in testing_data/pvalues.tsv.\n"

