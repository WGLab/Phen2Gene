# FIRST, set to wherever you would prefer your annovar DB be stored...if you don't have ANNOVAR already working for you
DATA=$HOME 
# download example variant file from paper mentioned in Phen2Gene manuscript (Figure 4)
wget http://molecularcasestudies.cshlp.org/content/suppl/2016/10/11/mcs.a001131.DC1/Supp_File_2_KBG_family_Utah_VCF_files.zip
unzip Supp_File_2_KBG_family_Utah_VCF_files.zip
rm -rf __MACOSX/;  rm Supp_File_2_KBG_family_Utah_VCF_files.zip
# assumes you have ANNOVAR and base Perl installed (http://annovar.openbioinformatics.org/en/latest/user-guide/download/)
# download all necessary ANNOVAR DBs
annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene $DATA/humandb/
annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ensGene $DATA/humandb/
annotate_variation.pl -buildver hg19 -downdb -webfrom annovar gnomad211_exome $DATA/humandb/
annotate_variation.pl -buildver hg19 -downdb -webfrom annovar gnomad211_genome $DATA/humandb/
annotate_variation.pl -buildver hg19 -downdb -webfrom annovar 1000g2015aug $DATA/humandb/
# annotate with gene names, functional consequence, and allele frequency information
table_annovar.pl File\ 2_KBG\ family\ Utah_VCF\ files/proband.vcf -buildver hg19 $DATA/humandb -out proband.annovar -remove -protocol refGene,ensGene,gnomad211_genome,gnomad211_exome,1000g2015aug_all -operation g,g,f,f,f -nastring . -vcfinput
# filter out common (>1% AF in gnomAD 2.1.1) variants
awk '$16 <= 0.01 || $16 == "."' FS="\t" proband.annovar.hg19_multianno.txt > filtered.proband.annovar.hg19_multianno.txt
# run Phen2Gene on HPO terms for this example patient
python phen2gene.py -f example/ANKRD11_id.txt -w sk -out ankrd11
# rerank Phen2Gene ranks based on genes present in variant file
python example/filterbyannovar.py -pre ankrd11/output_file.associated_gene_list -post ankrd11filter -anno filtered.proband.annovar.hg19_multianno.txt
# answer is in file ankrd11filter
head -10 ankrd11filter
