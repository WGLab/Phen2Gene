import networkx as nx 

jax_db = 'lib/JAX_DB/'
hpo = '../testing_data/hpo.obo'

def only_jax(gene_dict, hp_list):
    jax_gene = set()
    for hp in hp_list:
        try:
            for gene in open(jax_db + hp,'r'):
                jax_gene.add(gene.rstrip('\n'))
        except:
            pass
    jax_gene = list(jax_gene)
    print(str(len(jax_gene)))
    
    new_gene_dict = {}
    for gene in gene_dict.keys():
        
        #'''only takes those gene in JAX database and filter out 'predicted' genes'''
        if(gene_dict[gene][0] in jax_gene and gene_dict[gene][2] == 'SeedGene'):
        #'''only takes those gene in JAX database'''
        #if(gene_dict[gene][0] in jax_gene):
            new_gene_dict[gene] = gene_dict[gene]
            
            
    return new_gene_dict




def clean_term_data(HPid,xref,is_a,name,definition,is_obsolete,replaced_by,consider,alt_id,synonym,created_by, creation_date,comment, subset,property_value):
    HPid = ""
    xref = []
    synonym = []
    is_a = []
    name = ""

    definition = ""
    is_obsolete = False
    replaced_by = []
    consider = []
    alt_id = []

    created_by = ""
    creation_date = ""
    comment = ""
    subset = ""
    property_value = ""

    return (HPid,xref,is_a,name,definition,is_obsolete,replaced_by,consider,alt_id,synonym,created_by, creation_date,comment,subset,property_value)

def build_network():
    hpo_dg = nx.DiGraph()
    with open("./hpo.obo", "r") as fr:

        HPid = ""
        name = ""
        synonym = []
        xref = []
        is_a = []

        definition = ""
        is_obsolete = False
        replaced_by = []
        consider = []
        alt_id = []

        created_by = ""
        creation_date = ""
        comment = ""
        subset = ""
        property_value = ""

        new_term = "[Term]"

        hpo_headers = True

        for line in fr:
            if(line.startswith(new_term)):
                cnt_term += 1
                if(hpo_headers == True):
                    hpo_headers = False
                    (HPid,xref,is_a,name,definition,is_obsolete,replaced_by,consider,alt_id,synonym,created_by, creation_date,comment,subset,property_value) = clean_term_data(HPid,xref,is_a,name,definition,is_obsolete,
                                replaced_by,consider,alt_id,synonym,created_by, 
                                creation_date,comment,subset,property_value)
                    continue

                #update nodes
                node_updates = [(HPid, {'name':name, 'is_a':is_a, 'definition':definition, 'xref':xref, 'syn':synonym, 
                                'is_obsolete':is_obsolete, 'replaced_by':replaced_by,'consider':consider, 'alt_id':alt_id,
                                'created_by':created_by,'creation_date':creation_date, 'comment':comment, 'subset':subset})]
                #update edges
                edges_updates = []
                for parent in is_a:
                    edges_updates.append((HPid, parent))

                if(not is_obsolete):
                    hpo_dg.update(edges = edges_updates, nodes = node_updates)
                else:
                    hpo_dg.update(nodes=node_updates)

                (HPid,xref,is_a,name,definition,is_obsolete,replaced_by,consider,alt_id,synonym,created_by, creation_date,comment,subset,property_value) = clean_term_data(HPid,xref,is_a,name,definition,is_obsolete,
                                replaced_by,consider,alt_id,synonym,created_by, 
                                creation_date,comment,subset,property_value)
            elif(line.startswith("id: ")):
                HPid = line.rstrip("\n").split(": ")[1]
            elif(line.startswith("name: ")):
                name = line.rstrip("\n").split(": ")[1]
            elif(line.startswith("def: ")):
                definition = line.rstrip("\n").split("\"")[1]
            elif(line.startswith("synonym: ")):
                synonym.append( line.rstrip("\n").split("\"")[1])
            elif(line.startswith("is_a: ")):
                is_a.append( line.rstrip("\n").split(" ")[1])
            elif(line.startswith("alt_id: ")):
                alt_id.append( line.rstrip("\n").split(" ")[1])        
            elif(line.startswith("xref: ")):
                xref.append(line.rstrip("\n").split(" ")[1])
            elif(line.startswith("is_obsolete: ")):
                is_obsolete = True
            elif(line.startswith("consider: ")):
                consider.append(line.rstrip("\n").split(" ")[1])    
            elif(line.startswith("replaced_by: ")):
                replaced_by.append(line.rstrip("\n").split(" ")[1])
            elif(line.startswith("created_by: ")):
                created_by = line.rstrip("\n").split(" ")[1]
            elif(line.startswith("creation_date: ")):
                creation_date=line.rstrip("\n").split(" ")[1]
            elif(line.startswith("comment: ")):
                comment=line.rstrip("\n").split(": ")[1]
            elif(line.startswith("subset: ")):
                subset=line.rstrip("\n").split(" ")[1]
            elif(line.startswith("property_value: ")):
                property_value=line.rstrip("\n").split(": ")[1]

    return hpo_dg

'''
def skip_parent(hp_list, hpo_dg):
    parents = []
    
    for i in range(len(hp_list) ):
        for j in range(i, len(hp_list) ):
'''    
