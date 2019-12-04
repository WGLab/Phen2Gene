import os, sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-pre', '--pre_filter')
parser.add_argument('-post', '--post_filter')
parser.add_argument('-anno','--annovarfile')
args=parser.parse_args()


prefilter = args.pre_filter

annovarfile = args.annovarfile

postfilter = args.post_filter

annovagenes = set()
header = True
for line in open(annovarfile, 'r'):
	if(header):
		header = False
		continue
	gene = line.split('\t')[6]
	annovagenes.add(gene)


annovagenes = list(annovagenes)


fw = open(postfilter,'w+')

header = True
cnt = 1
for line in open(prefilter, 'r'):
	if(header):
		header = False
		fw.write(line)
		continue

	data = line.split('\t')
	
	gene = data[1]

	if(gene in annovagenes):
		fw.write('{}\t{}'.format(str(cnt), '\t'.join(data[1:])))
		cnt += 1

fw.close()


