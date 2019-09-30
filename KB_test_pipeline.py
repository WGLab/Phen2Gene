import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import errno
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--force', action='store_true')
args=parser.parse_args()


AJHG = 'testing_data/AJHG/'
CSH = 'testing_data/CSH/'
DGD = 'testing_data/DGD/'
CU = 'testing_data/ColumbiaU/'
TAF1 = 'testing_data/TAF1/'

probe_gene = 'testing_data/probe_info'

AJHG_probe_gene = {}
CSH_probe_gene = {}
CU_probe_gene = {}
DGD_probe_gene = {}

for line in open(probe_gene, 'r'):
    data = line.rstrip('\n').split('\t')
    if(data[0] == 'AJHG'):
        AJHG_probe_gene[data[1]] = data[2]
    elif(data[0] == 'CSH'):
        CSH_probe_gene[data[1]] = data[2]
    elif(data[0] == 'Columbia_U'):
        CU_probe_gene[data[1]] = data[2]
    elif(data[0] == 'DGD'):
        DGD_probe_gene[data[1]] = data[2]


AJHG_total_num = 83
CSH_total_num = 72
CU_total_num = 27
DGD_total_num = 85
TAF1_total_num = 14

AJHG_standards = [3.6, 8.4, 13.3, 19.3, 20.5, 28.9, 36.1]
CSH_standards = [16.7, 16.7, 19.4, 23.6, 30.6, 33.3, 41.7]
CU_standards  = [3.7, 11.1, 22.2, 22.2, 29.6, 37.0, 51.9]
DGD_standards  = [7.1, 18.8, 18.8, 21.2, 30.6, 35.3, 44.7]
TAF1_standards = [28.6, 71.4, 100.0, 100.0, 100.0, 100.0, 100.0]

AJHG_old_phenolyzer = [0,0,3.6,7.2]
CSH_old_phenolyzer = [20.8,23.6,23.6,25]
CU_old_phenolyzer  = [11.1,11.1,22.2,29.6]
DGD_old_phenolyzer  = [9.4,15.3,17.6,18.8]
TAF1_old_phenolyzer = [0.0,0.0,0.0,0.0]

AJHG_tops = [0,0,0,0,0,0,0]
CSH_tops = [0,0,0,0,0,0,0]
CU_tops = [0,0,0,0,0,0,0]
DGD_tops = [0,0,0,0,0,0,0]
TAF1_tops = [0,0,0,0,0,0,0]

AJHG_error_msg = {}
CSH_error_msg = {}
CU_error_msg = {}
DGD_error_msg = {}
TAF1_error_msg = {}

def run_data(data_set, tops, error_msg):
    
    data_set_probe_dict = None
    
    not_found = 0
    
    if(data_set == AJHG):
        data_set_probe_dict = AJHG_probe_gene
    elif(data_set == CSH):
        data_set_probe_dict = CSH_probe_gene
    elif(data_set ==CU):
        data_set_probe_dict = CU_probe_gene
    elif(data_set == DGD):
        data_set_probe_dict = DGD_probe_gene
    
    probe_gene_rank_dict = {}
    
    for f in os.listdir(data_set):
        error_msg[f] = ''
        probe_gene = 'TAF1'
        if(data_set != TAF1):
            probe_gene = data_set_probe_dict[f]
        output_name = 'out/' + f
        cmd = 'python phen2gene.py -f {} -w w -out {} -j'.format(data_set + f, output_name)
        print(cmd)
        try:
            if not os.path.isdir('out') or not os.listdir('out') or args.force:
                os.system(cmd)
                
            with open(output_name + "/output_file.associated_gene_list", "r") as fr1:

                line = fr1.readline()
                line = fr1.readline()
                found = False
                while(line):
                    if(line.split("\t")[1] == probe_gene):
                        found = True
                        rank = int(line.rstrip("\n").split('\t')[0])
                        #probe_gene_rank_dict[f] = data_row
                        if(rank <= 10):
                            tops[0] += 1
                        if(rank <= 25):
                            tops[1] += 1
                        if(rank <= 50):
                            tops[2] += 1
                        if(rank <= 100):
                            tops[3] += 1
                        if(rank <= 250):
                            tops[4] += 1
                        if(rank <= 500):
                            tops[5] += 1
                        if(rank <= 1000):
                            tops[6] += 1
                        break
                    line = fr1.readline()
                
                if(not found):
                    not_found += 1

        except Exception as e:
            error_msg[f] += str(e)
            return
    
    return not_found
    
def cmp(tops, standards):
    
    if(tops[0] > standards[0]):
        print('Top 10 gets better.')
    elif(tops[0] < standards[0]):
        print('top 10 get worse!')
    else:
        print('Top 10 doesn\'t change.')
        
    if(tops[1] > standards[1]):
        print('Top 25 gets better.')
    elif(tops[1] < standards[1]):
        print('top 25 get worse!')
    else:
        print('Top 25 doesn\'t change.')
        
    if(tops[2] > standards[2]):
        print('Top 50 gets better.')
    elif(tops[2] < standards[2]):
        print('top 50 get worse!')
    else:
        print('Top 50 doesn\'t change.')
        
    if(tops[3] > standards[3]):
        print('Top 100 gets better.')
    elif(tops[3] < standards[3]):
        print('top 100 get worse!')
    else:
        print('Top 100 doesn\'t change.')   
        
def print_error_msg(error_msg):
    no_error = True
    for f in error_msg.keys():
        if(len(error_msg[f]) > 0):
            no_error = False
            print(error_msg[f])
    if(no_error):
        print('No errors found.\n')

        
def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        
        
def plot(p2g, pheno, fig_name):
    p2g = p2g[0:4]
    x = np.arange(len(p2g))  # the label locations
    width = 0.35  # the width of the bars
    labels = ['Top 10', 'Top 25', 'Top 50', 'Top 100']
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, p2g, width, label='Phen2Gene')
    rects2 = ax.bar(x + width/2, pheno, width, label='Phenolyzer')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage')
    ax.set_title('Top Ranks')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1,ax)
    autolabel(rects2,ax)

    fig.tight_layout()

    plt.savefig(fig_name + '.png' , format='png')

def output_tsv(p2g, pheno, f_name):
    os.makedirs('rankings',exist_ok=True)
    with open('rankings/'+f_name + '.tsv', 'w+') as fw:
        fw.write('\tPhen2Gene\tPhenolyzer\n')
        fw.write('Top 10\t{}\t{}\n'.format(str(p2g[0]), str(pheno[0]) ))
        fw.write('Top 25\t{}\t{}\n'.format(str(p2g[1]), str(pheno[1]) ))
        fw.write('Top 50\t{}\t{}\n'.format(str(p2g[2]), str(pheno[2]) ))
        fw.write('Top 100\t{}\t{}\n'.format(str(p2g[3]), str(pheno[3]) ))

if args.force:
    rm_cmd = "rm -rf out"
    os.system(rm_cmd)
try:
    not_found_AJHG = run_data(AJHG, AJHG_tops, AJHG_error_msg)
    for i in range(len(AJHG_tops)):
        AJHG_tops[i] = round(AJHG_tops[i]/AJHG_total_num * 100, 1)
        
    not_found_CSH = run_data(CSH, CSH_tops,CSH_error_msg)
    for i in range(len(CSH_tops)):
        CSH_tops[i] = round(CSH_tops[i]/CSH_total_num * 100, 1)

    not_found_DGD = run_data(DGD, DGD_tops, DGD_error_msg)
    for i in range(len(DGD_tops)):
        DGD_tops[i] = round(DGD_tops[i]/DGD_total_num * 100, 1)

    not_found_TAF1 = run_data(TAF1, TAF1_tops, TAF1_error_msg)
    for i in range(len(TAF1_tops)):
        TAF1_tops[i] = round(TAF1_tops[i]/TAF1_total_num * 100, 1)

    not_found_CU = run_data(CU, CU_tops, CU_error_msg)
    for i in range(len(CU_tops)):
        CU_tops[i] = round(CU_tops[i]/CU_total_num * 100, 1)
except KeyError:
    print ("key error, missing file?")

print('\nTesting the new KnowledgeBase on AJHG data')
print_error_msg(AJHG_error_msg)
print(AJHG_tops)
cmp(AJHG_tops, AJHG_standards)
plot(AJHG_tops,AJHG_old_phenolyzer, 'AJHG')
output_tsv(AJHG_tops,AJHG_old_phenolyzer, 'AJHG')

print('\nTesting the new KnowledgeBase on CSH data') 
print_error_msg(CSH_error_msg)
print(CSH_tops)
cmp(CSH_tops, CSH_standards)
plot(CSH_tops,CSH_old_phenolyzer, 'CSH')
output_tsv(CSH_tops,CSH_old_phenolyzer, 'CSH')

print('\nTesting the new KnowledgeBase on DGD data') 
print_error_msg(DGD_error_msg)
print(DGD_tops)
cmp(DGD_tops, DGD_standards)
plot(DGD_tops,DGD_old_phenolyzer, 'DGD')
output_tsv(DGD_tops,DGD_old_phenolyzer, 'DGD')

print('\nTesting the new KnowledgeBase on TAF1 data')
print_error_msg(TAF1_error_msg)
print(TAF1_tops)
cmp(TAF1_tops, TAF1_standards)
plot(TAF1_tops[0:4],TAF1_old_phenolyzer, 'TAF1')
output_tsv(TAF1_tops[0:4],TAF1_old_phenolyzer, 'TAF1')

print('\nTesting the new KnowledgeBase on Columbia U data')
print_error_msg(CU_error_msg)
print(CU_tops)
cmp(CU_tops, CU_standards)
plot(CU_tops,CU_old_phenolyzer, 'CU')
output_tsv(CU_tops,CU_old_phenolyzer, 'CU')

print(str(not_found_AJHG))
print(str(not_found_CSH))
print(str(not_found_DGD))
print(str(not_found_TAF1))
print(str(not_found_CU))

AJHG_CSH_top = CSH_tops[0:4]
AJHG_CSH_old_phenolyzer = CSH_old_phenolyzer

for i in range(len(AJHG_CSH_top)):
    AJHG_CSH_top[i] += AJHG_tops[i]
    AJHG_CSH_old_phenolyzer[i] += AJHG_old_phenolyzer[i]

plot(AJHG_CSH_top, AJHG_CSH_old_phenolyzer, 'AJHG_CSH')
output_tsv(AJHG_CSH_top,AJHG_CSH_old_phenolyzer, 'AJHG_CSH')
