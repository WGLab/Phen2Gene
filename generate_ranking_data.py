#!/usr/bin/env python3

import os, argparse
import statistics as stat


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--causalgene', help='The file that stores causal gene info.', default='./testing_data/probe_info')
parser.add_argument('-f', '--force', action='store_true')
parser.add_argument('-p', '--phen2gene',help = 'The directory where it stores Phen2Gene outputs.', default='./testing_data/p2goutput')
parser.add_argument('-a', '--amelie', help='The directory where it stores Amelie outputs.', default='./testing_data/amelieoutput/amelieoutputs')
parser.add_argument('-g', '--gado', help='The directory where it stores GADO outputs.' , default='./testing_data/gadooutput')
parser.add_argument('-ph', '--phenolyzer',help = 'The directory where it stores Phenolyzer(v0.2.0) outputs.', default='./testing_data/phenolyzeroutput/phenoold')
parser.add_argument('-r', '--randomgene', help='The directory where it stores randomly selected genes for testing', default='./testing_data/random_gene_sets')
parser.add_argument('-o', '--out', help='The directory where it stores the rankings info for Phen2Gene vs. Phenolyzer vs. Amelie vs. GADO', default='./rankings')

args = parser.parse_args()
print(args)

if(args.amelie == None):
    print('Notice: You did not input the directory where it stores Amelie outputs.')
if(args.gado == None):
    print('Notice: You did not input the directory where it stores GADO outputs.')


os.system('mkdir -p {}'.format(args.out))


causaldict = {}
amelierank = {}
p2grank = {}
gadorank = {}
phenolyzerrank = {}


setnum = {'AJHG_CSH':0, 'DGD':0, 'TAF1':0, 'Columbia':0}

for line in open(r'{}'.format(args.causalgene)):
    data = line.rstrip('\n').split('\t')
    gene = data[2]
    case = data[1]
    if(case.startswith('TAF1')):
        case = case[4:]

    causaldict[case] = data[2]
    amelierank[case] = []
    p2grank[case] = []
    gadorank[case] = []
    phenolyzerrank[case] = []   


    if('sample' in case): setnum['DGD'] += 1
    elif('Colum' in case): setnum['Columbia'] += 1
    elif('case' in case): setnum['TAF1'] += 1
    else: setnum['AJHG_CSH'] += 1


### Run Phen2Gene for 282 testing cases. If those cases are already run and stored in 'args.phen2gene', this session will be skipped and the scripts continue to '### Analyzing data'
testing_folders = ['testing_data/AJHG', 'testing_data/CSH', 'testing_data/DGD', 'testing_data/ColumbiaU','testing_data/TAF1']

print('Checking if Phen2Gene has run all of the testing cases')

for folder in testing_folders:
    for case in os.listdir(folder):
        if( os.path.exists('{}/{}/output_file.associated_gene_list'.format(args.phen2gene, case)) and not args.force):
            print('{}, {} has been runned and the results are store in {}/{}/output_file.associated_gene_list'.format(folder.split('/')[1], case, args.phen2gene, case))
            continue
        phen2gene_cmd = 'python phen2gene.py -f {}/{} -w sk -out {}/{}'.format(folder, case, args.phen2gene, case)
        print('Phen2Gene is running for {} {}'.format(folder.split('/')[1], case))
        os.system(phen2gene_cmd)




### Analyzing data


geneset = {}
for i in range(1,11):
    geneset[i] = [line.rstrip('\n') for line in open(r'{}/unirandomselect_{}'.format(args.randomgene, str(i)))]


### Analyse Amelie outputs
print('Analysing Amelie outputs')

for i in range(1,11):
    afolder = '{}/uniamelie{}out'.format(args.amelie, str(i))
    
    
    for case in os.listdir(afolder):
        header = True
        genelist = []
        for line in open('{}/{}'.format(afolder, case)):
            if(header):
                header = False
                continue
            gene = line.rstrip('\n').lstrip('*')
            if(gene != causaldict[case] and gene not in geneset[i]): continue
            if(len(genelist) <1): 
                genelist.append(gene)
            
            if(gene in genelist): continue
            genelist.append(gene)
        cnt = 1000
        for k in range(len(genelist)):
            if(genelist[k] == causaldict[case]):
                cnt = k + 1
                break

        amelierank[case].append(cnt)




### Analyse Phen2Gene outputs
print('Analysing Phen2Gene outputs')

for case in causaldict.keys():
    if( not os.path.exists('{}/{}/output_file.associated_gene_list'.format(args.phen2gene,case))):
        print('Notice: Phen2Gene output file {} not exists'.format(case))
        continue
    header = True
    rawgene = []
    for line in open(r'{}/{}/output_file.associated_gene_list'.format(args.phen2gene,case)):
        if(header):
            header = False
            continue
        gene = line.split('\t')[1]
        rawgene.append(gene)



    for i in range(1,11):    
        genelst = []
        for j in range(len(rawgene)):
            if(rawgene[j] in geneset[i] or rawgene[j] == causaldict[case]):
                genelst.append(rawgene[j])
        
        cnt = 1000
        for k in range(len(genelst)):
            if(genelst[k] == causaldict[case]):
                cnt = k + 1
                break

        p2grank[case].append(cnt)



### Analyse GADO outputs
print('Analysing GADO outputs')

for case in causaldict.keys():
    if( not os.path.exists('{}/result/{}.txt'.format(args.gado, case))):
        print('Notice: GADO output file {} not exists'.format(case))
        continue

    initial_gene = []
    header = True
    for line in open(r'{}/result/{}.txt'.format(args.gado, case)):
        if(header):
            header = False
            continue
        gene = line.split('\t')[1]
        if(gene not in initial_gene):
            initial_gene.append(gene)

    for i in range(1,11):
        genelst = []
        for j in range(len(initial_gene)):
            if(initial_gene[j] in geneset[i] or initial_gene[j] == causaldict[case]):
                genelst.append(initial_gene[j])

        cnt = 1000
        for k in range(len(genelst)):
            if(genelst[k] == causaldict[case]):
                cnt = k + 1
                break

        gadorank[case].append(cnt)


### Analyse Phenolyzer outputs
print('Analysing Phenolyzer(v0.2.0)  outputs')

for case in causaldict.keys():
    if( not os.path.exists('{}/{}/out.final_gene_list'.format(args.phenolyzer, case))):
        print('Notice: Phenolyzer(v0.2.0) output file {} not exists'.format(case))
        continue

    initial_gene = []
    header = True
    for line in open(r'{}/{}/out.final_gene_list'.format(args.phenolyzer, case)):
        if(header):
            header = False
            continue
        gene = line.split('\t')[1]
        if(gene not in initial_gene):
            initial_gene.append(gene)

    for i in range(1,11):
        genelst = []
        for j in range(len(initial_gene)):
            if(initial_gene[j] in geneset[i] or initial_gene[j] == causaldict[case]):
                genelst.append(initial_gene[j])

        cnt = 1000
        for k in range(len(genelst)):
            if(genelst[k] == causaldict[case]):
                cnt = k + 1
                break

        phenolyzerrank[case].append(cnt)


mediandict = {}
for case in amelierank.keys():
    mediandict[case] = [1000,1000 , 1000, 1000]
    try:
        mediandict[case][0] =  round(stat.median(amelierank[case]))
    except:
        pass
    try:
        mediandict[case][1] =  round(stat.median(p2grank[case]))
    except:
        pass

    try:
        mediandict[case][2] =  round(stat.median(gadorank[case]))
    except:
        pass
    try:
        mediandict[case][3] =  round(stat.median(phenolyzerrank[case]))
    except:
        pass



top10 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
top50 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

top100 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
top250 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


for k in mediandict.keys():
    i = 0
    if('case' in k): i = 1 #TAF1
    elif('sample' in k): i = 2 #DGD
    elif('Colum' in k): i = 3 #Columbia
    else: i = 0 #AJHG + CSH
    for j in range(len(top10[0])):
        if(mediandict[k][j] <=10 ): top10[i][j] += 1
        #if(mediandict[k][1] <=10 ): top10[i][1] += 1
        if(mediandict[k][j] <=50 ): top50[i][j] += 1
        #if(mediandict[k][1] <=50 ): top50[i][1] += 1
        if(mediandict[k][j] <=100 ): top100[i][j] += 1
        #if(mediandict[k][1] <=100 ): top100[i][1] += 1
        if(mediandict[k][j] <=250 ): top250[i][j] += 1
        #if(mediandict[k][1] <=250 ): top250[i][1] += 1

tooldict = {'p2g': 1, 'amelie':0, 'gado':2, 'phenolyzer':3}

def tsvoutput(fname, top10, top50, top100, top250, idx, total):
    with open(fname,'w+') as fw:
        fw.write('\tPhen2Gene\tPhenolyzer\tAmelie\tGADO\n')
        fw.write('top10')
        fw.write('\t{}'.format(str(  round  (float( top10[idx][tooldict['p2g']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top10[idx][tooldict['phenolyzer']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top10[idx][tooldict['amelie']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top10[idx][tooldict['gado']] / total *100) , 1) )))
        fw.write('\n')
        fw.write('top50')
        fw.write('\t{}'.format(str(  round  (float( top50[idx][tooldict['p2g']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top50[idx][tooldict['phenolyzer']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top50[idx][tooldict['amelie']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top50[idx][tooldict['gado']] / total *100) , 1) )))
        fw.write('\n')

        fw.write('top100')
        fw.write('\t{}'.format(str(  round  (float( top100[idx][tooldict['p2g']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top100[idx][tooldict['phenolyzer']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top100[idx][tooldict['amelie'] ]/ total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top100[idx][tooldict['gado']] / total *100) , 1) )))
        fw.write('\n')
        fw.write('top250')
        fw.write('\t{}'.format(str(  round  (float( top250[idx][tooldict['p2g']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top250[idx][tooldict['phenolyzer']] / total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top250[idx][tooldict['amelie'] ]/ total *100) , 1) )))
        fw.write('\t{}'.format(str(  round  (float( top250[idx][tooldict['gado']] / total *100) , 1) )))
        fw.write('\n')






tsvoutput('{}/AJHG_CSH.tsv'.format(args.out), top10, top50, top100, top250, 0, setnum['AJHG_CSH'])
tsvoutput('{}/TAF1.tsv'.format(args.out), top10, top50, top100, top250, 1, setnum['TAF1'])
tsvoutput('{}/DGD.tsv'.format(args.out), top10, top50, top100, top250, 2, setnum['DGD'])
tsvoutput( '{}/CU.tsv'.format(args.out), top10, top50, top100, top250, 3, setnum['Columbia'])


