#!/bin/bash
#PBS -N pickle_dat
#PBS -q memroute
#PBS -l pmem=16gb
cd $HOME/assembly/coassembly/
./make_timing_pickle.py -i ../coassembly_test/ -n ../coassembly_test/NOTES.txt -o timing_results.pkl
