#!/bin/bash
#PBS -N coassembly
#PBS -q memroute
#PBS -l pvmem=32gb
#PBS -l nodes=1:ppn=16
#PBS -t 0-636
#PBS –j oe 
#PBS –e <file location>
/home/sawa6416/assembly/coassembly/test_cases/tc${PBS_ARRAYID}.sh
