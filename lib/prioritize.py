from collections import OrderedDict

def sort_dict(gene_dict):    

    gene_dict = OrderedDict(sorted(gene_dict.items(),  key=lambda kv:kv[1][1], reverse=True  ))
    return gene_dict
