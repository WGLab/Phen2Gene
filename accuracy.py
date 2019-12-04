import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
import sys
import argparse

# makes beautiful bar charts in the style of the CCR paper

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input", help = "TSV of top 10,50,100,250,500,1000 genes and scores")
parser.add_argument("-o", "--output", help = "output file name for plot")
parser.add_argument("-l", "--labels", nargs = 2, help = "labels for plot")
args = parser.parse_args()
infile = args.input
filename = args.output
labels = args.labels
if labels:
    label=labels[0]
    adlabel=labels[-1]
else:
    label="Phen2Gene"
    adlabel="Original Phenolyzer (ver. 0.2.2)"
scores = open(infile, "r")
ranks, phengene, phenolyzer = [],[],[]
next(scores)
for line in scores:
    fields = line.strip().split("\t")
    ranks.append(fields[0]); phengene.append(float(fields[1])); phenolyzer.append(float(fields[2]))


def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if height==1: # 2 for log2
            height=rect.get_y()
            ax.text(rect.get_x() + rect.get_width()/2., .65*height,
                    '%.1f' % float(height),
                    ha='center', va='bottom')
            continue
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.1f' % float(height),
                ha='center', va='bottom')

import seaborn as sns
sns.set_style('white')
matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rcParams['font.family'] = 'sans-serif'
#matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['font.size'] = 15

fig, ax = plt.subplots(1)

width=0.4
lefts=np.arange(0,1.2*len(ranks),1.2)
rects=ax.bar(x=lefts,height=phengene,width=width,tick_label=ranks,color=(161/255.0,218/255.0,215/255.0), edgecolor=(96/255.0, 133/255.0, 131/255.0),label=label)
autolabel(rects, ax)
# if max(phengene) > 10 or max(phenolyzer) > 10:
    # ax.set_yscale("log",basey=10,nonposy="clip")
    # ax.axhline(y=1, color='k')
# else:
    # ax.axhline(y=0, color='k')
#for i,o in enumerate(phengene):
#    ax.text(lefts[i]-width*.25, 0.14 if o<1 else 5, '%.3f' % phengene[i] if o<1 else '%.1f' % phengene[i], color='k', size=8)

alefts=np.arange(0+width,1.2*len(ranks)+width, 1.2)
rects=ax.bar(x=alefts,height=phenolyzer,width=width,tick_label=ranks,color=(56/255.0,138/255.0,172/255.0),edgecolor=(96/255.0, 133/255.0, 131/255.0),label=adlabel)
ax.set_xticks(alefts-width*.5)
autolabel(rects, ax)
#ax.set_title("Accuracy at Finding Causal Genes")
#ax.legend(loc='upper left')
fig.legend(loc='upper left', ncol=1,bbox_to_anchor=(0, 1.1))
#if max(phenolyzer) > 10:
    #for i,o in enumerate(phenolyzer):
     #   ax.text(alefts[i]-width*.25, 0.14 if o<1 else 5, '%.3f' % phenolyzer[i] if o<1 else '%.1f' % phenolyzer[i], color='k', size=8) #2 for log2

def mkdir_p(path):
    import os
    if not os.path.isdir(path):
        os.makedirs(path)

lims=ax.get_ylim()
ax.set_ylim(lims[0]/1.5, lims[1]+.4)
ax.set_xlabel("Ranked Gene Lists")
ax.set_ylabel("% of Cases with Causal Gene in List")
sns.despine()
mkdir_p("figures")
plt.savefig('figures/phen2gene'+filename+'.pdf', bbox_inches='tight')
