import numpy as np
import argparse
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser(description='Get that HPO distribution')
parser.add_argument('-f', "--file", help="file containing hpo terms linked to number of seed genes")
parser.add_argument('-o', "--output", help="output file name")
parser.add_argument('-t', "--title", help="Figure Title")

args = parser.parse_args()
data=pd.read_csv(args.file, sep="\t", header=0)
scores=data["Score"] # gets scores for each gene for an HPO term gene list inputted to this file
std=scores.std()
mean=scores.mean()

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns

ax = sns.distplot(scores,bins=100)
ax.set_xlabel("Raw Gene Score")
ax.set_ylabel("Frequency")
ax.set_title(args.title)
#ax.axvline(std, color='r',label=f"std={std:.2f}")
#ax.axvline(mean,color='b',label=f"mean={mean:.2f}")
#ax.legend(loc='upper right')

plt.savefig(args.output+'dist.png', bbox_inches='tight')
print(stats.skew(scores))
