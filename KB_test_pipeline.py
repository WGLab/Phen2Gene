import os

AJHG = 'test_pipeline/AJHG/'
CSH = 'test_pipeline/CSH/'
DGD = 'test_pipeline/DGD/'
CU = 'test_pipeline/ColumbiaU/'
TAF1 = 'test_pipeline/TAF1/'

probe_gene = 'test_pipeline/probe_info'

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

AJHG_tops = [0,0,0,0,0,0,0]
CSH_tops = [0,0,0,0,0,0,0]
CU_tops = [0,0,0,0,0,0,0]
DGD_tops = [0,0,0,0,0,0,0]
TAF1_tops = [0,0,0,0,0,0,0]



def run_data(data_set, tops):
    
    data_set_probe_dict = None
    
    
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
        probe_gene = 'TAF1'
        if(data_set != TAF1):
            probe_gene = data_set_probe_dict[f]
        output_name = 'out/' + f
        cmd = 'python phen2gene.py -f {} -w w -out {}'.format(data_set + f, output_name)
        #print(cmd)
        os.system(cmd)
        with open(output_name + "/output_file.associated_gene_list", "r") as fr1:
            
            line = fr1.readline()
            line = fr1.readline()
            while(line):
                if(line.split("\t")[1] == probe_gene):
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
            
                
        rm_cmd = "rm -r " + output_name
        os.system(rm_cmd)
    
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


run_data(AJHG, AJHG_tops)
for i in range(len(AJHG_tops)):
    AJHG_tops[i] = round(AJHG_tops[i]/AJHG_total_num * 100, 1)
    


run_data(CSH, CSH_tops)
for i in range(len(CSH_tops)):
    CSH_tops[i] = round(CSH_tops[i]/CSH_total_num * 100, 1)


'''
run_data(DGD, DGD_tops)
for i in range(len(DGD_tops)):
    DGD_tops[i] = round(DGD_tops[i]/DGD_total_num * 100, 1)
'''

run_data(TAF1, TAF1_tops)
for i in range(len(TAF1_tops)):
    TAF1_tops[i] = round(TAF1_tops[i]/TAF1_total_num * 100, 1)
    

run_data(CU, CU_tops)
for i in range(len(CU_tops)):
    CU_tops[i] = round(CU_tops[i]/CU_total_num * 100, 1)

print('\nTesting the new KnowledgeBase on AJHG data')
cmp(AJHG_tops, AJHG_standards)
print('\nTesting the new KnowledgeBase on CSH data') 
cmp(CSH_tops, CSH_standards)
#print('\nTesting the new KnowledgeBase on DGD data') 
#cmp(DGD_tops, DGD_standards)
print('\nTesting the new KnowledgeBase on TAF1 data')
cmp(TAF1_tops, TAF1_standards)
print('\nTesting the new KnowledgeBase on Columbia U data')
cmp(CU_tops, CU_standards)

