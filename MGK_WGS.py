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
output_file =  'MGK_typing.txt'
meningotype_path = '/srv/data/MPV/THEJ/Meningitis/meningotype/meningotype/meningotype/meningotype.py'
overview_file = '/srv/data/BIG/NGS_facility/analysis/Meningokokker/MGK_serotype_overview.txt'
cmd = meningotype_path+ ' --all '+input_file+' > '+output_file
previous_entries = []

with open(overview_file) as f:
	for line in f:
		if line[:9]!='SAMPLE_ID':
			line = line.rstrip('\n')
			line = line.split('\t')
			ID_string = '__'.join(line[:2])
			previous_entries.append(ID_string)
f.close()



if os.path.exists(input_file):
	os.system(cmd)




o = open(overview_file, "a")

if os.path.exists(output_file):
	with open(output_file) as f:
		for line in f:
			if line[:9]!='SAMPLE_ID':
				line = line.split('\t')
				print(run_ID[:6])
				if isolate_ID not in previous_entries and (run_ID[:6] == 'N_WGS_' or run_ID[:7] == 'M1_WGS_' or run_ID[:7] == 'M2_WGS_' or run_ID[:7] == 'MV_WGS_'):
					o.write(isolate_ID+'\t'+run_ID+'\t'+run_date+'\t'+'\t'.join(line[1:]))
	f.close()
o.close()

#print(previous_entries)