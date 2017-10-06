#!/usr/bin/env python3

import os
import sys

cwd = os.getcwd()
cwd_split = cwd.split('/')
isolate_ID = cwd_split[-1]
run_string = cwd_split[-2]
run_split = run_string.split('_')
run_date = run_split[0]
run_ID = '_'.join(run_split[3:6])

input_file = isolate_ID+'_contigs.fasta'
tmp_path = 'GAS_typing_blast_tmp'
blast_seqs = '/srv/data/MPV/THEJ/Streptococcus/EMM_typing/trimmed.tfa'
overview_file = '/srv/data/BIG/NGS_facility/analysis/Streptokokker/GAS_EMM-type_overview.txt'
output_file =  'GAS_typing.txt'
previous_entries = []

with open(overview_file) as f:
	for line in f:
		if line[:7]!='Isolate':
			line = line.rstrip('\n')
			line = line.split('\t')
			ID_string = '__'.join(line[:2])
			previous_entries.append(ID_string)
f.close()



alleles = {}
allelenames = []
alleleseqs = []

with open(blast_seqs) as f:
	for line in f:
		if line[0] == '>':
			line = line.rstrip('\n')
			line = line.split()
			type = line[0][1:]
			#print(type)
			alleles[type] = ''
		else:
			line = line.rstrip('\n')
			alleles[type] += line

for l in alleles:
	allelenames.append(l)
	alleleseqs.append(alleles[l])

if not os.path.exists(tmp_path):
	os.makedirs(tmp_path)

blast_path = os.path.join(tmp_path,'blast')
cmd = 'makeblastdb -out '+blast_path+' -dbtype nucl -in '+input_file
os.system(cmd)
blast_out = os.path.join(tmp_path,'blast_output.txt')
cmd = 'blastn -query /srv/data/MPV/THEJ/Streptococcus/EMM_typing/trimmed.tfa -db '+blast_path+' -num_descriptions 1 -num_alignments 1 -out '+blast_out+' -outfmt \"6 qseqid sseqid nident mismatch gaps bitscore\"'
os.system(cmd)


o = open(output_file, "w")
o.write('Isolate	EMM type	matches	mismatches	gaps\n')
ov = open(overview_file, "a")

with open(blast_out) as f:
	best_hit = 0
	for line in f:
		#print(line)
		line = line.rstrip('\n')
		line = line.split('\t')
		score = line[5]
		if float(score)>best_hit:
			emm_best = line
			best_hit = float(score)
	ID_string = isolate_ID+'__'+run_ID
	if emm_best[3] == '0' and emm_best[4] == '0':
		o.write(isolate_ID+'\t'+emm_best[0]+'\t'+emm_best[2]+'\t'+emm_best[3]+'\t'+emm_best[4]+'\n')
		if isolate_ID not in previous_entries and (run_ID[:6] == 'N_WGS_' or run_ID[:7] == 'M1_WGS_' or run_ID[:7] == 'M2_WGS_' or run_ID[:7] == 'MV_WGS_'):
			ov.write(isolate_ID+'\t'+run_ID+'\t'+run_date+'\t'+emm_best[0]+'\t'+emm_best[2]+'\t'+emm_best[3]+'\t'+emm_best[4]+'\n')
	else:
		o.write(isolate_ID+'\t*'+emm_best[0]+'\t'+emm_best[2]+'\t'+emm_best[3]+'\t'+emm_best[4]+'\n')
		if isolate_ID not in previous_entries and (run_ID[:6] == 'N_WGS_' or run_ID[:7] == 'M1_WGS_' or run_ID[:7] == 'M2_WGS_' or run_ID[:7] == 'MV_WGS_'):
			ov.write(isolate_ID+'\t'+run_ID+'\t'+run_date+'\t*'+emm_best[0]+'\t'+emm_best[2]+'\t'+emm_best[3]+'\t'+emm_best[4]+'\n')
f.close()

o.close()
ov.close()

cmd = 'rm -r '+tmp_path
os.system(cmd)
