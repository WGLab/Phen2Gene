# this will generate Figure 3, the accuracy comparison for benchmark sets
# between Phen2Gene and Original Phenolyzer
#### WILL SAVE TO FOLDER "figures" ####
python accuracy.py -f acccomparison/csh.tsv -o cshaccuracy
python accuracy.py -f acccomparison/TAF1.tsv -o TAF1accuracy
python accuracy.py -f acccomparison/columbiaU.tsv -o columbiaUaccuracy
python accuracy.py -f acccomparison/dgd.tsv -o dgdaccuracy
python accuracy.py -f acccomparison/ajhg.tsv -o ajhgaccuracy
