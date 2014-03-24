#!/bin/bash
#PBS -N coassembly
#PBS -joe
#PBS -q long
#PBS -l pmem=16gb
#PBS -l nodes=1:ppn=4
#PBS -o $HOME/assembly/coassembly_logs/coassembly_log437
$HOME/assembly/coassembly/test_cases/tc437.sh

