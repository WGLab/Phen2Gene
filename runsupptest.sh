#! usr/bin/sh
"""
printf "Dowloading the package for running the testing data in supplemental material....\n"

wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/supp_testing_package.zip
unzip -q supp_testing_package.zip -d testing_data
rm supp_testing_package.zip
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/jax.zip
unzip -q jax.zip -d testing_data/jax
rm jax.zip
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/weight.zip
unzip -q weight.zip -d testing_data/weights_methods
rm weight.zip
"""
printf "They are downloaded.\n"
printf "Analyzing the data for JAX weights....\n"

python testing_data/suppdataquick.py -t testing_data/probe_info -f testing_data/jax/out testing_data/jax/jax50 testing_data/jax/jax100 -he 'weight(JAX)=0.1' 'weight(JAX)=0.5' 'weight(JAX)=1.0'  -o jaxweights 

python testing_data/supp2.py -f jaxweights/TAF1.tsv -o TAF1_JAX_weights
python testing_data/supp2.py -f jaxweights/AJHG_CSH.tsv -o AJHG_CSH_JAX_weights
python testing_data/supp2.py -f jaxweights/Columbia.tsv -o CU_JAX_weights
python testing_data/supp2.py -f jaxweights/DGD.tsv -o DGD_JAX_weights

printf "Analyzing the data for different weighting methods....\n"

python testing_data/suppdataquick.py -t testing_data/probe_info -f testing_data/weights_methods/out testing_data/weights_methods/weighted testing_data/weights_methods/unweighted -he 'Skewness' 'Ontology-based Information Contente' 'Unweighted'  -o weighting_methods

python testing_data/supp1.py -f weighting_methods/TAF1.tsv -o TAF1_weighting_methods
python testing_data/supp1.py -f weighting_methods/AJHG_CSH.tsv -o AJHG_CSH_weighting_methods
python testing_data/supp1.py -f weighting_methods/Columbia.tsv -o CU_weighting_methods
python testing_data/supp1.py -f weighting_methods/DGD.tsv  -o DGD_weighting_methods




