#!/usr/bin/sh

###### Downlaod benchmark data
printf "Running the testing data......\n"
mkdir -p rankings


##### Downlaod testing data
printf "Downloading testing data....\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/testing_data.zip
unzip -q testing_data.zip -d ./ 
rm testing_data.zip
printf "Testing data downloaded...\n"


printf "Dowloading the testing data for Phenolyzer(v 0.2.0), GADO, and Amelie.......\n"


wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/p2goutput.zip -O p2goutput.zip && unzip -q p2goutput.zip -d testing_data
rm p2goutput.zip


wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/pheno.zip -O pheno.zip && unzip -q  pheno.zip -d testing_data/phenolyzeroutput
rm pheno.zip
printf "The testing data for Phenolyzer(v 0.2.0) is downloaded.\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/gadoresult.zip -O gadoresult.zip && unzip -q gadoresult.zip -d testing_data/gadooutput
rm gadoresult.zip
printf "The testing data for GADO is downloaded.\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/amelie.zip -O amelie.zip && unzip -q amelie.zip -d testing_data/amelieoutput
rm amelie.zip
printf "The testing data for Amelie is downloaded.\n"


printf "Running Phen2Gene for the testing data and analyze the result of Phen2Gene, Phenolyzer(v 0.2.0), GADO, and Amelie......\n"

python generate_ranking_data.py -pv  > generate_ranking_data.log && echo "Finished." && echo "tsv files are in rankings/\n" && echo "Generating figures.......\n" && sh accuracy.sh


##### Download supplemental data 
printf "Downloading the package for running the testing data in supplemental material....\n"
### Downloading supplemental material
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/supp_testing_package.zip -O supp_testing_package.zip && unzip -qo supp_testing_package.zip -d testing_data && rm supp_testing_package.zip



wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/jax.zip -O jax.zip && unzip -qo jax.zip -d testing_data/jax && rm jax.zip


wget -q  https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/weight.zip -O weight.zip && unzip -qo weight.zip -d testing_data/weights_methods && rm weight.zip

printf "They are downloaded.\n"
printf "Analyzing the data for JAX weights (out of 20k genes)....\n"
### out of 20k
python testing_data/suppdataquick.py -t testing_data/probe_info -f testing_data/jax/out testing_data/jax/jax50 testing_data/jax/jax100 -he 'weight(JAX)=0.1' 'weight(JAX)=0.5' 'weight(JAX)=1.0'  -o rankings/jaxweights

python testing_data/supp2.py -f rankings/jaxweights/TAF1.tsv -o TAF1_JAX_weights
python testing_data/supp2.py -f rankings/jaxweights/AJHG_CSH.tsv -o AJHG_CSH_JAX_weights
python testing_data/supp2.py -f rankings/jaxweights/Columbia.tsv -o CU_JAX_weights
python testing_data/supp2.py -f rankings/jaxweights/DGD.tsv -o DGD_JAX_weights

printf "Analyzing the data for different weighting methods (out of 20k genes)....\n"
### out of 20k
python testing_data/suppdataquick.py -t testing_data/probe_info -f testing_data/weights_methods/out testing_data/weights_methods/weighted testing_data/weights_methods/unweighted -he 'Skewness' 'Ontology-based Information Contente' 'Unweighted'  -o rankings/weighting_methods

python testing_data/supp1.py -f rankings/weighting_methods/TAF1.tsv -o TAF1_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods/AJHG_CSH.tsv -o AJHG_CSH_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods/Columbia.tsv -o CU_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods/DGD.tsv  -o DGD_weighting_methods

### out of 1k
printf "Analyzing the data for JAX weights (out of 1k genes)....\n"

python testing_data/suppdata.py -t testing_data/probe_info -f testing_data/jax/out testing_data/jax/jax50 testing_data/jax/jax100 -he 'weight(JAX)=0.1' 'weight(JAX)=0.5' 'weight(JAX)=1.0'  -o rankings/jaxweights1k -g testing_data/random_gene_sets

python testing_data/supp2.py -f rankings/jaxweights1k/TAF1.tsv -o TAF1_JAX_weights1k
python testing_data/supp2.py -f rankings/jaxweights1k/AJHG_CSH.tsv -o AJHG_CSH_JAX_weights1k
python testing_data/supp2.py -f rankings/jaxweights1k/Columbia.tsv -o CU_JAX_weights1k
python testing_data/supp2.py -f rankings/jaxweights1k/DGD.tsv -o DGD_JAX_weights1k
### out of 1k
printf "Analyzing the data for different weighting methods (out of 1k genes)....\n"
python testing_data/suppdata.py -t testing_data/probe_info -f testing_data/weights_methods/out testing_data/weights_methods/weighted testing_data/weights_methods/unweighted -he 'Skewness' 'Ontology-based Information Contente' 'Unweighted'  -o rankings/weighting_methods1k -g testing_data/random_gene_sets

python testing_data/supp1.py -f rankings/weighting_methods1k/TAF1.tsv -o TAF1_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods1k/AJHG_CSH.tsv -o AJHG_CSH_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods1k/Columbia.tsv -o CU_weighting_methods
python testing_data/supp1.py -f rankings/weighting_methods1k/DGD.tsv  -o DGD_weighting_methods

printf "Supplemental data tests finished. Ther figures are in 'figures/'\n"

##### Download noise data and run noise test
printf "Starting the noise test.\n"
printf "Noise 1 is Seizure (HP:0001250)\n"
printf "Noise 2 is Macrodontia (HP:0001572)\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/noisetest.zip
unzip -q noisetest.zip -d testing_data
rm noisetest.zip

### Running noise tests and generating TSV files
python testing_data/noisetest.py -n 'HP:0001250' 'HP:0001572' -no 'testing_data/HP:0001250_output' 'testing_data/HP:0001572_output' -he 'No noise' 'Noise=Seizure (HP:0001250)' 'Noise=Macrodontia (HP:0001572)'

printf "Noise tests finished.\n Generating figures...\n"
### Generating figure
python testing_data/supp3.py -f testing_data/noisetest/AJHG_CSH.tsv -o noiseAJHG_CSH &
python testing_data/supp3.py -f testing_data/noisetest/TAF1.tsv -o noiseTAF1 &
python testing_data/supp3.py -f testing_data/noisetest/DGD.tsv -o noiseDGD &
python testing_data/supp3.py -f testing_data/noisetest/Columbia.tsv -o noiseColumbia &

printf "Noise test finished. \n"

### pvalue tests
printf "Calculating p-values....\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/pvalues.zip -O pvalues.zip && unzip -qo pvalues.zip -d testing_data && rm pvalues.zip

python testing_data/pvalue.py -s testing_data/signtest_pvaluesAJHG_CSH.tsv testing_data/signtest_pvaluesTAF1.tsv testing_data/signtest_pvaluesDGD.tsv testing_data/signtest_pvaluesColumbia.tsv -o testing_data/pvalues.tsv -he 'Phen2Gene vs Phenolyzer' 'Phen2Gene vs Amelie' 'Phen2Gene vs GADO'
printf "p-values are stored in testing_data/pvalues.tsv.\n"



printf "Finished."


