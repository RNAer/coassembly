#!/usr/bin/env python
import os 
import re
from itertools import combinations

test_case_prefix = './test_cases/tc' 
input_dir = '/compy-home/sawa6416/assembly/hand_selected_strains/'
output_dir = '/compy-home/sawa6416/assembly/hand_selected_strains/'
run_idba = True
idba = '/compy-home/sawa6416/tools/idba-1.1.1/bin/idba_ud' 
fq2fa = '/compy-home/sawa6416/tools/idba-1.1.1/bin/fq2fa'
interleave = '/compy-home/sawa6416/bin/interleave-fasta.py'
pwd = os.getcwd()

#output = open('test_cases.txt', 'w')
notes = open('test_case_notes.txt', 'w')

""" file_pairs becomes a list of all paired-end read files """ 
file_pairs = []
for fastq in os.listdir(input_dir):
    if fastq.endswith("1.fq.gz"):
        file_pairs.append( (fastq, \
            re.sub(r'1.fq.gz$', '2.fq.gz', fastq)))

i = 0 
for n in xrange(1, 6):
    for test_set in combinations(file_pairs, n):
        output = open(test_case_prefix + str(i) + '.sh', 'w')
        output.write('#!/bin/bash\n')
        cmds = [] 
        dir_name = output_dir+'idba_out_'+str(i)+'/'
        files1 =' '.join([input_dir+pair[0] for pair in test_set])
        files2 =' '.join([input_dir+pair[1] for pair in test_set])
        cmds.append('mkdir ' + dir_name)
        cmds.append('cat %s > %s1.fq.gz' % (files1, dir_name))
        cmds.append('cat %s > %s2.fq.gz' % (files2, dir_name))
        #cmds.append(fq2fa + (' --merge %s1.fq.gz %s2.fq.gz %sseqs.fasta' \
        #    % (dir_name, dir_name, dir_name)))
        # fq2fa not working... ugh.

        # Workaround: unzip, convert, merge
        cmds.append('gunzip %s1.fq.gz' % (dir_name))
        cmds.append('gunzip %s2.fq.gz' % (dir_name))
        cmds.append('fastq_to_fasta -i %s1.fq -o %s1.fa' % (dir_name, dir_name))
        cmds.append('fastq_to_fasta -i %s2.fq -o %s2.fa' % (dir_name, dir_name))
        cmds.append(interleave + ' %s1.fa %s2.fa > %sseqs.fasta' % \
            (dir_name, dir_name, dir_name))
        # Clean up
        cmds.append('rm %s1.fa' % (dir_name))
        cmds.append('rm %s2.fa' % (dir_name))
        cmds.append('rm %s1.fq' % (dir_name))
        cmds.append('rm %s2.fq' % (dir_name))

        cmds.append(idba + ' -r %sseqs.fasta -o %s' % (dir_name, dir_name))
        cmds.append('rm %sseqs.fasta' % (dir_name))
        output.write('\n'.join(cmds)+'\n')
        output.close()
        notes.write('%d: %s\n' % (i, ', '.join([pair[0] for pair in test_set])))
        i = i + 1

notes.close()

