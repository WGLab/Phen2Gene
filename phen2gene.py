#!/usr/bin/env python

import sys
import os
import argparse

from lib.prioritize import gene_prioritization
from lib.output import write_list as write_list_tsv
from lib.json_format import write_list as write_list_json
from lib.weight_assignment import assign
from lib.calculation import calc, calc_simple
from lib.filter import only_jax

knowledgebase = "./lib/Knowledgebase/"

HP_file_suffix=".candidate_gene_list"

weight_model = ""

HPO_id = []

# Define commande line arguments
parser = argparse.ArgumentParser(description='Phen2Gene: Phenotype driven gene prioritization tool.\n  Phen2Gene take input data (HPO, Human Phenotype Ontology), and output a prioritized suspected gene list.')

parser.add_argument('-f', '--file', metavar='FILE.NAME',  help='Input file(s) of HP IDs.', nargs='*')

parser.add_argument('-ud', '--user_defined', metavar='TERM&WEIGHT',  help='Input file(s) of HP IDs and user-defined weights.', nargs='*')

parser.add_argument('-m', '--manual', metavar='HPID',  help='Input HPO ID(s) one by one, seperated by an empty space.', nargs='*')

parser.add_argument('-w', '--weight_model', metavar='w|u|s|ic|d', help='Methods to merge gene scores.\n \'w\' ( Default ) Scoring by weighted Human-Phenotype terms\n \'u\'  Scoring by Unweighted Human-Phenotype terms')

parser.add_argument('-v', '--verbosity', action='store_true', help='Display Phen2Gene workflow verbosely.')

parser.add_argument('-wo', '--weight_only', action='store_true', help='Output weights of HPO terms only.')

parser.add_argument('-out', '--output',  help='Specify the path to store output files.\n Default directory path: ./out/', default="out/")

parser.add_argument('-n', '--name', metavar='output.file.name', help='Name the output file.')

parser.add_argument('-json', '--json', action='store_true', help='Output the file in json format.')

parser.add_argument('-j', '--jax_only', action='store_true', help='Select those gene only in JAX HPO database.')

args = parser.parse_args()

files = args.file
manuals = args.manual
output_path= args.output
weight_model = args.weight_model

user_defineds = args.user_defined
output_file_name = args.name

json_formatting = args.json

# If no HPO ID(s) available, exit the scripts.
if(files == None and manuals == None and user_defineds == None):
    print("\n\nPlease input a file, or manually input HPO ID(s).\n\n", file=sys.stderr)
    parser.print_help()
    sys.exit("")

if(output_path == None):
    output_path = "./out/"
if(not output_path.endswith("/")):
    output_path += "/"

# read what weighting model user input. Information content is the default model.
if(user_defineds != None):
    weight_model = 'd'
else:
    if( weight_model == None or (weight_model.lower() != 'u' and weight_model.lower() != 's' and weight_model.lower() != 'w' ) ):
        weight_model = 'ic'

# Print info of weighting model on terminal, if verbosity
if(args.verbosity):
    if(weight_model.lower() == 'w'):
        print("\nHPO weighting model: Intuitive\n")
        #weight_model = 'intuitive'
    elif(weight_model.lower() == 'u' or weight_model.lower() == 's'):
        print("\nHPO weighting model: None\n")
        #weight_model = 'none'
    elif(weight_model.lower() == 'ic'):
        print("\nHPO weighting model: Ontology-based Informatin Content\n")
        #weight_model = 'ic_sanchez'
    else:
        print("\nHPO weighting model: User-defined\n")




# Analyze user-defined output path, and create the output path if it is not created

path_list = output_path.split("/")

if(path_list[0] == ""):
    path_list[0] = "."
    output_path = "." + output_path
    
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

    
# Define deflaut output file name, if user did not enter it.
if( output_file_name == None):
    output_file_name = "output_file" 

# Collect manually input HPO ID
if(manuals != None and weight_model != 'd'):
    for HP_item in manuals:
        # Simple check if HPO ID or not
        if(HP_item.startswith("HP:") and len(HP_item) == 10 and HP_item[3:].isnumeric()):
            HPO_id.append(HP_item)
        else:
            if(args.verbosity):
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
# HPO weights are determined by weighting models
else:
    for hp in HPO_id:
        (weight, replaced_by) = assign(hp,weight_model)
        if(weight >0):
            if(replaced_by != None):
                hp_weight_dict[replaced_by] = weight
            else:
                hp_weight_dict[hp] = weight

### Only outputs HP id's weights
if(args.weight_only):
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
    gene_dict = calc_simple(hp_weight_dict, args.verbosity)
else:
    gene_dict = calc(hp_weight_dict, args.verbosity)
    

    
### filter out those genes not in JAX DB
if(args.jax_only):
    print('select those genes only in jax')
    gene_dict = only_jax(gene_dict, hp_weight_dict.keys())

    
### output the final prioritized associated gene list
# Prioritize all found genes
gene_dict = gene_prioritization(gene_dict)

# output the sorted gene list
if(json_formatting):
    write_list_json(output_path, output_file_name, weight_model.lower() ,gene_dict)
else:
    
    write_list_tsv(output_path, output_file_name, weight_model.lower() ,gene_dict)
                    
print("Finished.")
print("Output path: " + output_path  + "\n")  

'''
# Read gene data in each HPO ID(s) in Knowledgebase
if(method_input == 'w'):
    for HP_term in HPO_id:
        if(args.verbosity == True):
            print("\nReading " + HP_term + HP_file_suffix + " from HPO2Gene Knowledgebase...")
        score_merge.extract_HP_data_weighted_HPO(knowledgebase + HP_term + HP_file_suffix, gene_dict, args.verbosity)
elif(method_input == 'u'):
    for HP_term in HPO_id:
        if(args.verbosity == True):
            print("\nReading " + HP_term + HP_file_suffix + " from HPO2Gene Knowledgebase...")
        score_merge.extract_HP_data_unweighted_HPO(knowledgebase + HP_term + HP_file_suffix, gene_dict, args.verbosity)

else:
    for HP_term in HPO_id:
        if(args.verbosity == True):
            print("\nReading " + HP_term + HP_file_suffix + " HPO2Gene from Knowledgebase...")
        score_merge.simple_extract_HP_data(knowledgebase + HP_term + HP_file_suffix, gene_dict, args.verbosity)

'''


   


