import numpy as np
import argparse
import pandas as pd
from scipy import stats
import os

parser = argparse.ArgumentParser(description='Get that HPO distribution')
parser.add_argument('-d', "--dir", help="dir containing hpo terms linked to number of seed genes")
parser.add_argument('-f', "--file", help="get the distribution of raw score for an HPO term.")
parser.add_argument('-o', "--output", help="output file name")
args = parser.parse_args()

o = open(args.output, "w")
path=os.path.abspath(args.file)
directory=os.listdir(args.file)


data = pd.read(path, sep="\t", header=0)
score = data['Score']
#skew = stats.skew(data["Score"])

std=score.std()
mean=score.mean()

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns

sns.distplot(score,bins=40)
plt.axvline(std, color='r',label=f"std={std:.2f}")
plt.axvline(mean,color='b',label=f"mean={mean:.2f}")
plt.legend(loc='upper right')

plt.savefig(args.output+'dist.png', bbox_inches='tight')
print(stats.skew(score))




