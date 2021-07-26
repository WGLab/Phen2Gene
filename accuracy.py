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
parser.add_argument("-l", "--labels", nargs = 4, help = "labels for plot")
args = parser.parse_args()
infile = args.input
filename = args.output
labels = args.labels

if( not labels):
    labels = ['Phen2Gene', 'Original Phenolyzer (ver. 0.2.2)', 'Amelie', 'GADO']
    

while(len(labels) < 4):
    labels.append('label{}'.format(str(len(labels))))

'''
if labels:
    label=labels[0]
    adlabel=labels[-1]
else:
    label="Phen2Gene"
    adlabel="Original Phenolyzer (ver. 0.2.2)"
'''
scores = open(infile, "r")
ranks, phengene, phenolyzer, amelie, gado = [],[],[],[],[]
next(scores)
for line in scores:
    fields = line.strip('\n').split("\t")
    #print(line)
    ranks.append(fields[0]); phengene.append(round(float(fields[1]),1));phenolyzer.append(float(fields[2]));amelie.append(float(fields[3]));gado.append(float(fields[4]))


def autolabel(rects, ax, yoffset=0, xoffset=0):
    """
    Attach a text label above each bar displaying its height
    """
    global filename
    for rect in rects:
        height = rect.get_height()
        if height==1: # 2 for log2
            height=rect.get_y()
            ax.text(rect.get_x() + rect.get_width()/2., .65*height,
                    '%.1f' % float(height),
                    ha='center', va='bottom')
            continue
        if('TAF1' in filename):
            ax.text(rect.get_x() + rect.get_width()/2., 0.9*height + yoffset,
                '%.1f' % float(height),
                ha='center', va='bottom', fontweight='bold')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.1f' % float(height),
                ha='center', va='bottom', fontweight='bold')

import seaborn as sns
sns.set_style('white')
matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rcParams['font.family'] = 'sans-serif'
#matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['font.size'] = 11

fig, ax = plt.subplots(1)

width=0.4
distance = 2
lefts=np.arange(0,distance*len(ranks),distance)
rects=ax.bar(x=lefts,height=phengene,width=width,tick_label=ranks,color=(161/255.0,218/255.0,215/255.0), edgecolor=(96/255.0, 133/255.0, 131/255.0),label=labels[0])
if('TAF1' in filename):
    autolabel(rects, ax, -6, -0.1)

else:

    autolabel(rects, ax, xoffset=-0.2)


alefts=np.arange(0+width,distance*len(ranks)+width, distance)




rects=ax.bar(x=alefts,height=phenolyzer,width=width,tick_label=ranks,color=(56/255.0,138/255.0,172/255.0),edgecolor=(96/255.0, 133/255.0, 131/255.0),label=labels[1])
ax.set_xticks(alefts-width*.5)


autolabel(rects, ax)


#ax.set_title("Accuracy at Finding Causal Genes")
#ax.legend(loc='upper left')

alefts=np.arange(0+2*width,distance*len(ranks)+2*width, distance)
rects=ax.bar(x=alefts,height=amelie,width=width,tick_label=ranks,color=(95/255.0,158/255.0,160/255.0),edgecolor=(96/255.0, 133/255.0, 131/255.0),label=labels[2])
ax.set_xticks(alefts-width*.5)
if('TAF1' in filename):
    autolabel(rects, ax, -6)

else:

    autolabel(rects, ax)





alefts=np.arange(0+3*width,distance*len(ranks)+3*width, distance)
rects=ax.bar(x=alefts,height=gado,width=width,tick_label=ranks,color=(135/255.0,206/255.0,250/255.0),edgecolor=(96/255.0, 133/255.0, 131/255.0),label=labels[3])
ax.set_xticks(alefts- width*1.5)

autolabel(rects, ax, xoffset=0.1)


fig.legend(loc='upper left', ncol=1,bbox_to_anchor=(0, 1.1))

def mkdir_p(path):
    import os
    if not os.path.isdir(path):
        os.makedirs(path)

lims=ax.get_ylim()
if('TAF1' in filename):
   # print(lims)
    ax.set_ylim(lims[0]/1.5, lims[1]*1.11)
else:
    ax.set_ylim(lims[0]/1.5, lims[1]+.4)
ax.set_xlabel("Ranked Gene Lists", fontsize=15)
ax.set_ylabel("% of Cases with Causal Gene in List", fontsize=14.5)
sns.despine()
mkdir_p("figures")
plt.savefig('figures/phen2gene'+filename+'.png', bbox_inches='tight')
