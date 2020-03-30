#!/usr/bin/sh

printf "Running the testing data......\n"
mkdir -p rankings

printf "Downloading testing data....\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/testing_data.zip
unzip -q testing_data.zip -d ./ 
rm testing_data.zip
printf "Testing data downloaded...\n"

printf "Dowloading the testing data for Phenolyzer(v 0.2.0), GADO, and Amelie.......\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/pheno.zip
unzip -q  pheno.zip -d testing_data/phenolyzeroutput
rm pheno.zip
printf "The testing data for Phenolyzer(v 0.2.0) is downloaded.\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/gadoresult.zip
unzip -q gadoresult.zip -d testing_data/gadooutput
rm gadoresult.zip
printf "The testing data for GADO is downloaded.\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/amelie.zip
unzip -q amelie.zip -d testing_data/amelieoutput
rm amelie.zip
printf "The testing data for Amelie is downloaded.\n"



printf "Running Phen2Gene for the testing data and analyze the result of Phen2Gene, Phenolyzer(v 0.2.0), GADO, and Amelie......\n"

python generate_ranking_data.py -f  > generate_ranking_data.log && echo "Finished." && echo "tsv files are in rankings/\n" && echo "Generating figures.......\n" && sh accuracy.sh

printf "Finished."


