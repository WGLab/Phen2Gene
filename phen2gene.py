#!/usr/bin/env python3

import sys
import os
import argparse
import io

from lib.prioritize import gene_prioritization
from lib.output import write_list as write_list_tsv
from lib.json_format import write_list as write_list_json
from lib.weight_assignment import assign
from lib.calculation import calc, calc_simple

def main():
    # path of HPO2Gene KnowledgeBase
    KBpath = None

    try:
        with open(sys.path[0]+'/lib/h2gpath.config') as fr:
            KBpath = fr.readline().rstrip('\n')
    except:
        pass


    if(KBpath is None or not os.path.exists(KBpath)):
        sys.exit('The path of the HPO2Gene KnowledgeBase cannot be found, or you have not installed HPO2Gene KnowledgeBase.\nRun \'bash setup.sh\' to install HPO2Gene KnowledgeBase.')

    HP_file_suffix = ".candidate_gene_list"

    weight_model = ""


    # Define commande line arguments
    parser = argparse.ArgumentParser(description='Phen2Gene: Phenotype driven gene prioritization tool.\n  Phen2Gene take input data (HPO, Human Phenotype Ontology), and output a prioritized suspected gene list.')

    parser.add_argument('-f', '--file', metavar='FILE.NAME', help='Input file(s) of HP IDs.', nargs='*')

    parser.add_argument('-ud', '--user_defined', metavar='TERM&WEIGHT', help='Input file(s) of HP IDs and user-defined weights.', nargs='*')

    parser.add_argument('-m', '--manual', metavar='HPID', help='Input HPO ID(s) one by one, separated by an empty space.', nargs='*')

    parser.add_argument('-w', '--weight_model', metavar='w|u|s|ic|d', help='Methods to merge gene scores.\n \'w\' ( Default ) Scoring by weighted Human-Phenotype terms\n \'u\'  Scoring by Unweighted Human-Phenotype terms')

    parser.add_argument('-v', '--verbosity', action='store_true', help='Display Phen2Gene workflow verbosely.')

    parser.add_argument('-wo', '--weight_only', action='store_true', help='Output weights of HPO terms only.')

    parser.add_argument('-out', '--output',  help='Specify the path to store output files.\n Default directory path: ./out/', default="out/")

    parser.add_argument('-n', '--name', metavar='output.file.name', help='Name the output file.')

    parser.add_argument('-json', '--json', action='store_true', help='Output the file in json format.')

    parser.add_argument('-g', '--gene_weight', action='store_true', help='Apply the weights for genes.')

    parser.add_argument('-c', '--cutoff', action='store_true', help='cut off weights of some selected gene.')

    parser.add_argument('-l', '--genelist', help='1 column text file of potential disease genes (OPTIONAL, NOT REQUIRED)')

    parser.add_argument('-d', '--database', help='tells Phen2Gene where the H2GKB is stored (if custom install or on Windows, may be necessary)')

    args = parser.parse_args()

    if args.database:
        KBpath = args.database
        print (KBpath)

    files = args.file
    manuals = args.manual
    user_defineds = args.user_defined
    
    weight_model = args.weight_model
    weight_only = args.weight_only

    output_path = args.output
    output_file_name = args.name

    json_formatting = args.json
    gene_weight = args.gene_weight

    cutoff = args.cutoff

    verbosity = args.verbosity

    genelist = args.genelist

    results(KBpath, files, manuals, user_defineds, weight_model, weight_only, output_path, output_file_name, json_formatting, gene_weight, cutoff, genelist, verbosity, cl=True)


# cl argument is true if run on command line
def results(KBpath, files=None, manuals=None, user_defineds=None, weight_model=None, weight_only=False, output_path=None, output_file_name=None, json_formatting=False, gene_weight=None, cutoff=None, genelist=None, verbosity=False, cl=True):

    HPO_id = []

    # If no HPO ID(s) available, exit the scripts.
    if cl and files == None and manuals == None and user_defineds == None:
        print("\n\nPlease input a file, or manually input HPO ID(s).\n\n", file=sys.stderr)
        parser.print_help()
        sys.exit("")

    # read what weighting model user input. Skewness is the default model.
    if(user_defineds != None):
        weight_model = 'd'
    else:
        if( weight_model == None or (weight_model.lower() != 'u' and weight_model.lower() != 's' and weight_model.lower() != 'ic' and weight_model.lower() != 'w') ):
            weight_model = 'sk'

    # only for command line
    if cl:
        # Print info of weighting model on terminal, if verbosity
        if verbosity:
            if(weight_model.lower() == 'w'):
                print("\nHPO weighting model: Intuitive\n")
                #weight_model = 'intuitive'
            elif(weight_model.lower() == 'u' or weight_model.lower() == 's'):
                print("\nHPO weighting model: None\n")
                #weight_model = 'none'
            elif(weight_model.lower() == 'ic'):
                print("\nHPO weighting model: Ontology-based Informatin Content\n")
                #weight_model = 'ic_sanchez'
            elif(weight_model.lower() == 'sk'):
                print("\nHPO weighting model: Skewness\n")
                #weight_model = 'ic_sanchez'
            else:
                print("\nHPO weighting model: User-defined\n")

        # Analyze user-defined output path, and create the output path if it is not created
        if(output_path == None):
            output_path = "./out/"
        if(not output_path.endswith("/")):
            output_path += "/"

        path_list = output_path.split("/")

        if(path_list[0] == "."):
            for i in range(1,len(path_list)):
                path_name = "./"
                for j in range(1,i):
                    path_name += path_list[j] + "/"
                path_name += path_list[i]
                # Create folder hierarchically
                if(not os.path.isdir(path_name) ):
                    os.mkdir(path_name)
        else:
            
            for i in range(0,len(path_list)):
                path_name = "./"
                for j in range(0,i):
                    path_name += path_list[j] + "/"
                path_name += path_list[i]
                # Create folder hierarchically
                if(not os.path.isdir(path_name) ):
                    os.mkdir(path_name)
            
        # Define default output file name, if user did not enter it.
        if( output_file_name == None):
            output_file_name = "output_file" 


    # redirect stdout to new_stdout (get printed output as a variable) 
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    # Collect manually input HPO ID
    if(manuals != None and weight_model != 'd'):
        for HP_item in manuals:
            # Simple check if HPO ID or not
            if(HP_item.startswith("HP:") and len(HP_item) == 10 and HP_item[3:].isnumeric()):
                HPO_id.append(HP_item.replace(':','_'))
            else:
                if(verbosity):
                    print(HP_item, "is not a valid HPO ID,", sep = " ")

    # Extract HPO ID from input files
    if(files != None and weight_model != 'd'):
        for file_item in files:
            try:
                with open(file_item, "r") as one_file:
                    print("Reading", file_item, "...", "\n", sep = " ")
                    entire_data = one_file.read()
                    HP_data = entire_data.split("\n")
                    for HP in HP_data:
                        # Simply check if HPO ID or not
                        if(HP.startswith("HP:") and len(HP) == 10 and HP[3:].isnumeric()):
                            # Change HP id format from 'HP:nnnnnnn' to 'HP_nnnnnnn', since ':' is an illegal character in file names in MacOS ans Windows system
                            HPO_id.append(HP.replace(":","_"))
            except FileNotFoundError:
                print("\n"+ file_item + " not found!\n", file=sys.stderr)

    ## Create a dict to store weights of HPO terms
    hp_weight_dict = {}
    # If HPO weights are pre-defined by users
    if(weight_model == 'd'):
        if(user_defineds != None):
            for file_item in user_defineds:
                try:
                    with open(file_item, "r") as one_file:
                        entire_data = one_file.read()
                        entire_data = entire_data[:-1]
                        HP_weight_data = entire_data.split("\n")
                        for HP_weight in HP_weight_data:
                            
                            hp_weight = HP_weight.split("\t")
                            # Change HP id format from 'HP:nnnnnnn' to 'HP_nnnnnnn', since ':' is an illegal character in file names in MacOS ans Windows system
                            hp = hp_weight[0]
                            hp = hp.replace(":","_",1)
                            hp_weight_dict[hp] = float(hp_weight[1])
                            
                except FileNotFoundError:
                    print("\n"+ file_item + " not found!\n", file=sys.stderr)
    #elif(weight_model == 'sk'):
        
    # HPO weights are determined by weighting models
    else:
        for hp in HPO_id:
            (weight, replaced_by) = assign(KBpath, hp,weight_model)
            if(weight >0):
                if(replaced_by != None):
                    hp_weight_dict[replaced_by] = weight
                else:
                    hp_weight_dict[hp] = weight

    ### Only outputs HP id's weights
    if(weight_only):
        with open(output_path + output_file_name + ".HP_weights", "w+") as fw:
            fw.write("HP ID\tWeight\n")
            for hp in hp_weight_dict.keys():
                fw.write(hp + "\t" + str(hp_weight_dict[hp]) + "\n")
        print("Finished.")
        print("Output path: " + output_path  + "\n") 
        exit()

    ### down_weighting
    #hp_weight_dict = down_weight(hp_weight_dict)
        
    # Create a dict to store associated gene data
    if(weight_model.lower() == 's'):
        gene_dict = calc_simple(KBpath, hp_weight_dict, verbosity)
    else:
        gene_dict = calc(KBpath, hp_weight_dict, verbosity, gene_weight, cutoff)
        
    std_output = new_stdout.getvalue()
    # reset stdout
    sys.stdout = old_stdout

    if cl:
        print(std_output)

    ### if user inputs a candidate gene list, remove all genes but candidate genes
    if(genelist):
        with open(genelist) as f:
            genelist = [line.strip() for line in f]
        for key in genelist:
            if key not in gene_dict.keys():
                gene_dict[key] = [key, 0, 'Not in KB', 0, "NA"]
        unwanted = set(gene_dict.keys()) - set(genelist)
        for unwanted_key in unwanted:
            del gene_dict[unwanted_key]

    ### output the final prioritized associated gene list
    # Prioritize all found genes
    gene_dict = gene_prioritization(gene_dict)

    if cl:
        # output the sorted gene list
        if(json_formatting):
            write_list_json(output_path, output_file_name, weight_model.lower(), gene_dict)
        else:
            write_list_tsv(output_path, output_file_name, weight_model.lower(), gene_dict)
                    
        print("Finished.")
        print("Output path: " + output_path  + "\n")  

    else:
        return gene_dict, std_output, weight_model


if __name__ == "__main__":
    main()
