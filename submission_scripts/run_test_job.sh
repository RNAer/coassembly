#!/bin/bash
#PBS -N coassembly
#PBS -joe
#PBS -q memroute
#PBS -l pvmem=64gb
#PBS -l nodes=1:ppn=2
#PBS -o /home/sawa6416/assembly/coassembly_logs/coassembly_log
/home/sawa6416/assembly/coassembly/test_cases/tc636.sh
