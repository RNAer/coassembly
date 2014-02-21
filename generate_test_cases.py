#!/usr/bin/env python
import os 
import re
from itertools import combinations

""" This script generates test cases in the form of bash scripts 
    to run a collection of sequencing reads through several 
    assembly programs (IDBA, SPades, and Minia, at the moment.)

    The program combines and assembles all possible combinations 
    of the supplied read sets, from 1 (single set) up to 
    max_combine (inclusive), specified below.

    Some assemblers require different input formats, so 
    code is in place to create and remove temporary files as needed. 

    What to specify:
"""

# ---------------------------------------------------------------------
#  Configuration of input/output/executable paths and program options
# ---------------------------------------------------------------------
max_combine = 5
home_dir = '/compy-home/sawa6416/' # for easier switching from compy/s10
test_case_dir = './test_cases/'
test_case_prefix = test_case_dir + 'tc' 
test_case_notes = test_case_dir + 'NOTES.txt' 
input_dir = home_dir + 'assembly/hand_selected_strains/'
output_dir = home_dir + 'assembly/coassembly_test/'
interleave = home_dir + 'bin/interleave-fasta.py'
quast = 'python ' + home_dir + 'tools/quast-2.3/quast.py'

""" Specify and select specific assemblers """ 
# IDBA 
idba = home_dir + 'tools/idba-1.1.1/bin/idba_ud' 
run_idba = True

# SPades
spades = home_dir + 'tools/SPAdes-3.0.0-Linux/bin/spades.py'
run_spades = True 

# Minia 
minia = home_dir + 'tools/minia-1.6088/minia'
run_minia = True
minia_kmer = 31
minia_min = 3
minia_size_est = 5000000 # 5MBp 

# ---------------------------------------------------------------------

file_pairs = []
for fastq in os.listdir(input_dir):
    if fastq.endswith("1.fq.gz"):
        file_pairs.append( (fastq, \
            re.sub(r'1.fq.gz$', '2.fq.gz', fastq)))

i = 0 
notes = open(test_case_notes, 'w')

for n in xrange(1, max_combine+1):
    for test_set in combinations(file_pairs, n):
        """ Loop over all combinations of 1 to max_combine 
            mixed genomes """ 
        output = open(test_case_prefix + str(i) + '.sh', 'w')
        output.write('#!/bin/bash\n')
        cmds = [] 
        contigs = [] 

        test_case_dir = output_dir+'test_case_'+str(i)+'/'
        files1 =' '.join([input_dir+pair[0] for pair in test_set])
        files2 =' '.join([input_dir+pair[1] for pair in test_set])
        cmds.append('\n#---------- PREPARATION -------------')
        cmds.append('mkdir ' + test_case_dir)
        cmds.append('cat %s > %s1.fq.gz' % (files1, test_case_dir))
        cmds.append('cat %s > %s2.fq.gz' % (files2, test_case_dir))
   
        if run_idba: 
            """ IDBA requires an interleaved FASTA file for the sequences 
                Need to create that from the pair of FASTQ files.
            """ 
            cmds.append('\n#---------- RUN IDBA -------------')
            # fq2fa not working... ugh.
            #fq2fa = '/compy-home/sawa6416/tools/idba-1.1.1/bin/fq2fa'
            #cmds.append(fq2fa + (' --merge %s1.fq.gz %s2.fq.gz %sseqs.fasta' \
            #    % (test_case_dir, test_case_dir, test_case_dir)))
            # Workaround: unzip, convert, merge (slow and annoying)
            cmds.append('gunzip -c %s1.fq.gz > %s1.fq' % (test_case_dir,test_case_dir))
            cmds.append('gunzip -c %s2.fq.gz > %s2.fq' % (test_case_dir,test_case_dir))
            cmds.append('fastq_to_fasta -i %s1.fq -o %s1.fa' % (test_case_dir, test_case_dir))
            cmds.append('fastq_to_fasta -i %s2.fq -o %s2.fa' % (test_case_dir, test_case_dir))
            cmds.append(interleave + ' %s1.fa %s2.fa > %sseqs.fasta' % \
                (test_case_dir, test_case_dir, test_case_dir))

            # Run IDBA 
            idba_dir = test_case_dir + 'out_idba/'
            cmds.append('mkdir -p ' + idba_dir)
            cmds.append(idba + ' -r %sseqs.fasta -o %s' % (test_case_dir, idba_dir))
            cmds.append('rm %sseqs.fasta' % (test_case_dir))
            cmds.append('rm %s1.fq' % (test_case_dir)) # Get rid of gunzipped files
            cmds.append('rm %s2.fq' % (test_case_dir))
            cmds.append('rm %s1.fa' % (test_case_dir)) # Get rid of fasta files
            cmds.append('rm %s2.fa' % (test_case_dir))

        if run_spades: 
            cmds.append('\n#---------- RUN SPADES -------------')
            spades_dir = test_case_dir + 'out_spades/'
            cmds.append('mkdir -p ' + spades_dir)
            cmds.append(spades + (' --pe1-1 %s1.fq.gz --pe1-2 %s2.fq.gz ' % \
                (test_case_dir, test_case_dir)) + '-o ' + spades_dir)

        if run_minia:
            cmds.append('\n#---------- RUN MINIA -------------')
            minia_dir = test_case_dir + 'out_minia/'
            cmds.append('mkdir -p ' + minia_dir)
            cmds.append('cat %s1.fq.gz %s2.fq.gz > %scombined.fq.gz' \
                % (test_case_dir, test_case_dir, test_case_dir))
            cmds.append(minia + ' %scombined.fq.gz %d %d %d %sout' % \
                (test_case_dir, minia_kmer, minia_min, minia_size_est, minia_dir))
            cmds.append('rm -f %scombined.fq.gz' % (test_case_dir))

        cmds.append('\n#---------- CLEAN UP -------------')
        cmds.append('rm %s1.fq.gz' % (test_case_dir))
        cmds.append('rm %s2.fq.gz' % (test_case_dir))

        # Write all commands to test case script 
        output.write('\n'.join(cmds)+'\n')
        output.close()
        notes.write('%d: %s\n' % (i, ', '.join([pair[0] for pair in test_set])))
        i = i + 1

notes.close()

