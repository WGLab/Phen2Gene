KB = "./lib/Knowledgebase/"

def calc(hp_weight_list, verbosity):
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
                        gene_dict[gene_id] = [data[1], hp_weight_list[hp]*float(data[3]), data[4]]
                    else:
                        gene_dict[gene_id][1] += hp_weight_list[hp]*float(data[3])
                        if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                            gene_dict[gene_id][2] = "SeedGene"
                    line = HP_file.readline()
        except FileNotFoundError:
            if(verbosity):
                print(hp + " is not a valid HPO term. cal")
                
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