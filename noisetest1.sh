#! /usr/bin/sh

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

printf "Finished.\n"

