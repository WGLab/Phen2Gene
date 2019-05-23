import sys


def weighted_extract_HP_data(HP_gene_list, gene_dict, verbosity):
    HP_gene_list = HP_gene_list.replace('HP:', 'HP_')

    try:
        with open(HP_gene_list, "r") as HP_file:
            line = HP_file.readline()
            line = HP_file.readline()
            line = HP_file.readline()
            while(line ):
                data = line.strip("\n").split("\t")
                gene_id = int(data[2])
                if(gene_dict.get(gene_id) == None):
                    gene_dict[gene_id] = [data[1], float(data[3]), data[4]]
                else:
                    gene_dict[gene_id][1] += float(data[3])
                    if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                        gene_dict[gene_id][2] = "SeedGene"
                line = HP_file.readline()

        #return gene_dict
    except FileNotFoundError:
        if(verbosity):
            pos = HP_gene_list.find("HP:")
            print("\n" + HP_gene_list[pos:pos+10] + " is not a valid HPO ID.", file=sys.stderr)
        else:
            pass

def extract_HP_data_weighted_HPO(HP_gene_list,gene_dict, verbosity):
    try:
        with open(HP_gene_list, "r") as HP_file:
            line = HP_file.readline()
            weight_data = line.strip("\n").split("\t")
            weight = float(weight_data[1])
            #print(weight)
            line = HP_file.readline()
            line = HP_file.readline()
            while(line ):
                data = line.strip("\n").split("\t")
                gene_id = int(data[2])
                if(gene_dict.get(gene_id) == None):
                    gene_dict[gene_id] = [data[1], weight * float(data[3]), data[4]]
                else:
                    gene_dict[gene_id][1] += weight * float(data[3])
                    if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                        gene_dict[gene_id][2] = "SeedGene"
                line = HP_file.readline()

        #return gene_dict
    except FileNotFoundError:
        if(verbosity):
            pos = HP_gene_list.find("HP_")
            print("\n" + HP_gene_list[pos:pos+10] + " is not a valid HPO ID.", file=sys.stderr)
        else:
            pass

def simple_extract_HP_data(HP_gene_list, gene_dict, verbosity):
    HP_gene_list = HP_gene_list.replace('HP:', 'HP_')
    try:
        with open(HP_gene_list, "r") as HP_file:
            line = HP_file.readline()
            line = HP_file.readline()
            line = HP_file.readline()
            while(line):
                data = line.strip("\n").split("\t")
                gene_id = int(data[2])
                if(gene_dict.get(gene_id) == None):
                    gene_dict[gene_id] = [data[1], 1, data[4]]
                else:
                    gene_dict[gene_id][1] += 1
                    if(data[4] == "SeedGene" and gene_dict[gene_id][2] == "Predicted"):
                        gene_dict[gene_id][2] = "SeedGene"
                line = HP_file.readline()

        #return gene_dict
    except FileNotFoundError:
        if(verbosity):
            pos = HP_gene_list.find("HP_")
            print("\n" + HP_gene_list[pos:pos+10] + " is not a valid HPO ID.", file=sys.stderr)
        else:
            pass
                    