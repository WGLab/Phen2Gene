import numpy as np
import argparse
import pandas as pd
from scipy import stats
import os

parser = argparse.ArgumentParser(description='Get that HPO distribution')
parser.add_argument('-d', "--dir", help="dir containing hpo terms linked to number of seed genes")
parser.add_argument('-o', "--output", help="output file name")
args = parser.parse_args()

o = open(args.output, "w")
path=os.path.abspath(args.dir)
directory=os.listdir(args.dir)
for d in directory:
    data=pd.read_csv("/".join([path,d])+"/out.final_gene_list", sep="\t", header=0)
    skew = stats.skew(data["Score"])
    print("\t".join([d,f"{skew:.2f}"]),file=o)
