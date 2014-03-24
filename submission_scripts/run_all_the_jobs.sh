#!/bin/bash
#PBS -N coassembly
#PBS -joe
#PBS -q long
#PBS -l pmem=16gb
#PBS -l nodes=1:ppn=4
#PBS -t 100-636
#PBS -o $HOME/assembly/coassembly_logs/coassembly_log
$HOME/assembly/coassembly/test_cases/tc${PBS_ARRAYID}.sh

