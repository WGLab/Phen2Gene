#!/usr/bin/env python3

outdated_HP = "lib/outdated_HP/"

def assign(KBpath, hp, model='ic', replaced_by = None):
    
    db_weight = '{}/{}'.format(KBpath, 'weights/')
    skewnessfiles = '{}/{}'.format(KBpath, 'skewness/')
    # Check HP id format should be 'HP_nnnnnnn'
    if(hp[2] == ":"):
        hp = hp.replace(":", "_",1)

    try:
       if(model == 'ic' or model == 'w'):
            with open(db_weight + hp, "r") as fr:
                data = fr.read().split("\n")
                if(model == 'ic'):
                    return (float(data[1]), replaced_by)
                if(model == 'w'):
                    return (float(data[2]), replaced_by)
       elif(model == 'sk'):
           with open(skewnessfiles + hp, "r") as fr:
                data = fr.read().rstrip('\n').split("\t")
                return (float(data[0]), replaced_by)
       else:
           return (1.0, replaced_by)
    except FileNotFoundError:
        try:
            with open(outdated_HP + hp, "r") as fr:
                
                data = fr.read().split("\n")
                
                # this outdated HP is replaced by another HP, so assign it the weight of the new HP.
                if(len(data[1]) >0):
                    print(hp.replace("_",":") +" ("+ data[0] +")" +" is obsolete, and replaced by "+ data[1].replace("_",":") +".\nPhen2Gene gave the weight of "+ data[1].replace("_",":") + " to " + hp.replace("_",":")+" .")
                    return assign(KBpath,data[1], model, data[1])
                
                # this HPO term is outdated. It have references to other currently valid HPO terms
                if(len(data[2]) >0):
                    print(hp.replace("_",":") +" ("+ data[0] +")" + " is obsolete.\nPhen2Gene skipped it.")
                    refs = data[2].split(",")
                    
                    for ref in refs:
                        print("Consider: " + ref.replace("_",":"))
                    return (0, None)
        except FileNotFoundError:
            pass
        print(hp.replace("_", ":",1) + " is not a valid human phenotype.\nPhen2Gene skipped it.")
        return (0, None)
        
