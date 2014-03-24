#!/bin/bash
#PBS -N coassembly_SMALL
#PBS -joe
#PBS -q long
#PBS -l pmem=16gb
#PBS -l nodes=1:ppn=4
#PBS -t 0-9
#PBS -o $HOME/assembly/coassembly_logs/coassembly_small_test
$HOME/assembly/coassembly/test_cases/tc${PBS_ARRAYID}.sh
