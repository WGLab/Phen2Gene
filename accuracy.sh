# this will generate Figure 3, the accuracy comparison for benchmark sets
# between Phen2Gene and Original Phenolyzer
#### WILL SAVE TO FOLDER "figures" ####
#python accuracy.py -f rankings/CSH.tsv -o cshaccuracy
python accuracy.py -f rankings/TAF1.tsv -o TAF1accuracy
python accuracy.py -f rankings/CU.tsv -o columbiaUaccuracy
python accuracy.py -f rankings/DGD.tsv -o dgdaccuracy
#python accuracy.py -f rankings/AJHG.tsv -o ajhgaccuracy
python accuracy.py -f rankings/AJHG_CSH.tsv -o ajhg_cshaccuracy
