import numpy as np
import argparse
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser(description='Get that HPO distribution')
parser.add_argument('-f', "--file", help="file containing hpo terms linked to number of seed genes")
parser.add_argument('-o', "--output", help="output file name")

args = parser.parse_args()
data=pd.read_csv(args.file, sep="\t", header=0)
data=data[data["top1000"]>0] # filters out genes with no influence, like IGK or pseudogenes
std=data["top100"].std()
mean=data["top100"].mean()

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns

sns.distplot(data["top100"],bins=40)
plt.axvline(std, color='r',label=f"std={std:.2f}")
plt.axvline(mean,color='b',label=f"mean={mean:.2f}")
plt.legend(loc='upper right')

plt.savefig(args.output+'dist.png', bbox_inches='tight')
print(stats.skew(data["top100"]))
