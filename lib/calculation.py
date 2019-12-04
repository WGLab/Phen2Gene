KB = "./lib/Knowledgebase/"

def calc(hp_weight_list, verbosity, gene_weight, cutoff):
    gene_dict = {}
    hp_num = len(hp_weight_list)

    hp_downweight_lst = []
    downweight = 0.5
    #for line in open(r'./lib/hpgt350'):
    #    hp_downweight_lst.append(line.rstrip('\n').replace(':','_'))


    for hp in hp_weight_list.keys():
        
        try:
            with open(KB + hp + ".candidate_gene_list", "r") as HP_file:
                line = HP_file.readline()
                line = HP_file.readline()
                while(line ):
                    data = line.strip("\n").split("\t")
                    #if(len(data) < 3):
                    #    line = HP_file.readline()
                    #    continue
                    # try to apply 'hpgt350'
                    #if(hp in hp_downweight_lst):
                        #data[3] = downweight * float(data[3])
                    gene_id = int(data[2])
                    if(gene_dict.get(gene_id) == None):
                        # key:gene_id  value: [gene_name, score, 'seedgene/predicted']}
                        gene_dict[gene_id] = [data[1], hp_weight_list[hp]*float(data[3]), data[4], 0]
                    else:
                        gene_dict[gene_id][1] += hp_weight_list[hp]*float(data[3])
                        gene_dict[gene_id][3] += 1
                        if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                            gene_dict[gene_id][2] = "SeedGene"

                    line = HP_file.readline()
        except FileNotFoundError:
            if(verbosity):
                print(hp + " is not a valid HPO term. cal")
    '''
    for gene_id in gene_dict.keys():
        #print(str(gene_id))
        if(gene_dict[gene_id][3] < p20):
            gene_dict[gene_id][1] *= 3
            #print('{} : {}'.format(gene_dict[gene_id][0], str(gene_dict[gene_id][1])))
        elif(gene_dict[gene_id][3] < p50):
            gene_dict[gene_id][1] *= 2
    '''
    if(cutoff):
        if(len(gene_dict) > 0):
            top100lst = []

            #lt10gt0 = []
            #for line in open(r'./lib/genetop10'):
            for line in open(r'./lib/gt311top100'):
 
                top100lst.append(line.rstrip('\n'))

            #for line in open(r'./lib/lt10gt0'):
            #    lt10gt0.append(line.rstrip('\n'))

            for gene_id in gene_dict.keys():
                if(gene_dict[gene_id][0] in top100lst):
                    gene_dict[gene_id][1] *= 0.5
                #if(gene_dict[gene_id][0] in lt10gt0):
                #    gene_dict[gene_id][1] *= 2
    if(gene_weight):
        for geneid in gene_dict.keys():
            weight = 0
            with open('./lib/geneweight/{}'.format(gene_dict[geneid][0]), 'r') as fr:
                weight = float(fr.read().rstrip('\n'))

            gene_dict[geneid][1] *= weight
    return gene_dict



def calc_simple(hp_weight_list, verbosity):
    gene_dict = {}
    for hp in hp_weight_list.keys():
        
        try:
            with open(KB + hp + ".candidate_gene_list", "r") as HP_file:
                line = HP_file.readline()
                line = HP_file.readline()
                while(line ):
                    data = line.strip("\n").split("\t")
                    gene_id = int(data[2])
                    if(gene_dict.get(gene_id) == None):
                        # key:gene_id  value: [gene_name, score, 'seedgene/predicted']}
                        gene_dict[gene_id] = [data[1], 1, data[4]]
                    else:
                        gene_dict[gene_id][1] += 1
                        if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                            gene_dict[gene_id][2] = "SeedGene"
                    line = HP_file.readline()
        except FileNotFoundError:
            if(verbosity):
                print(hp + " is not a valid HPO term. cal")
                
    return gene_dict
