#!/usr/bin/env python

import sys
import os
import argparse

from lib import score_merge
from lib import prioritize
from lib import output

# Define commande line arguments
parser = argparse.ArgumentParser(description='Phen2Gene: Phenotype driven gene prioritization tool.\n  Phen2Gene take input data (HPO, Human Phenotype Ontology), and output a prioritized suspected gene list.')

parser.add_argument('-f', '--file', metavar='FILE.NAME',  help='Input HPO as file.', nargs='*')

parser.add_argument('-m', '--manual', metavar='HPID',  help='Input HPO ID(s) one by one, seperated by an empty space.', nargs='*')

parser.add_argument('-w', '--method', metavar='w|u', help='Methods to merge gene scores.\n \'w\' ( Default ) Scoring by weighted Human-Phenotype terms\n \'u\'  Scoring by Unweighted Human-Phenotype terms')

parser.add_argument('-v', '--verbosity', action='store_true', help='Display Phen2Gene workflow verbosely.')

parser.add_argument('-out', '--output',  help='Specify the path to store output files.\n Default directory path: ./out/', default="out/")

args = parser.parse_args()

file_input  =args.file
manual_input = args.manual
output_input = args.output
method_input = args.method


# If no HPO ID(s) available, exit the scripts.
if(file_input == None and manual_input == None):
    print("\n\nPlease input a file, or manually input HPO ID(s).\n\n", file=sys.stderr)
    parser.print_help()
    sys.exit("")

if(output_input == None):
    output_input = "./outout/"
if(not output_input.endswith("/")):
    output_input += "/"

# Set Weighted Score Merge as the Default method
if( method_input == "U"):
    method_input = 'u'
elif(method_input == "S"):
    method_input = 's'
if( method_input != 'u' and method_input != 's'):
    method_input = 'w'


if(args.verbosity):
    if(method_input == 'w'):
        print("\nGene scoring method: Scoring by Weighted Human-Phenotype terms \n")
    elif(method_input == 'u'):
        print("\nGene scoring method: Scoring by Unweighted Human-Phenotype terms \n")
    else:
        print("\nGene scoring method: Scoring by Simple Merge \n")


HPO_id = []

knowledgebase = "./lib/Knowledgebase/"

HP_file_suffix=".candidate_gene_list"



case_name = ""




path_list = output_input.split("/")
if(path_list[0] == ""):
    path_list[0] = "."
    output_input = "." + output_input
if(path_list[0] == "."):
    for i in range(1,len(path_list)):
        path_name = "./"
        for j in range(1,i):
            path_name += path_list[j] + "/"
        path_name += path_list[i]
        #print("path_name" + path_name)
        if(not os.path.isdir(path_name) ):
            os.mkdir(path_name)
else:
    
    for i in range(0,len(path_list)):
        path_name = "./"
        for j in range(0,i):
            path_name += path_list[j] + "/"
        path_name += path_list[i]
        #print("path_name" + path_name)
        if(not os.path.isdir(path_name) ):
            os.mkdir(path_name)

    

if(case_name == ""):
    case_name = "input_case" 

# Collect manually input HPO ID
if(manual_input != None):
    for HP_item in manual_input:
        # Simple check if HPO ID or not
        if(HP_item.startswith("HP:") and len(HP_item) == 10 and HP_item[3:].isnumeric()):
            HPO_id.append(HP_item)
        else:
            if(args.verbosity):
             print(HP_item, "is not a valid HPO ID,", sep = " ")


gene_dict = dict({})


# Extract HPO ID from input files
if(file_input != None):
    for file_item in file_input:
        try:
            with open(file_item, "r") as one_file:
                entire_data = one_file.read()
                HP_data = entire_data.split("\n")
                for HP in HP_data:
                    # Simple check if HPO ID or not
                    if(HP.startswith("HP:") and len(HP) == 10 and HP[3:].isnumeric()):
                        HPO_id.append(HP)
        except FileNotFoundError:
            print("\n"+ file_item + " not found!\n", file=sys.stderr)

# Read gene data in each HPO ID(s) in Knoeledgebase
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


# Prioritize all found genes
gene_dict = prioritize.sort_dict(gene_dict)

# Output the final genelist
output.build_output_file(output_input, case_name, method_input,gene_dict)
                    

print("\nPath to final candidate gene list: " + output_input  + "\n")     


