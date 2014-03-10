#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Sam Way", "Rob Knight"] 
__license__ = "GPL"
__version__ = "1.8.0-dev"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

import argparse
import brewer2mpl
from numpy import array
from lib.parse import load
import matplotlib.pyplot as plt

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--timing-results-pickle', help='Timing results pickle', required=True)
    args = args.parse_args()
    return args

def make_timing_plots(timing_dict):
    plot_key = 'time_wall'

    combined_results = {} 
    
    for res_idx, timing_results in timing_dict.iteritems():
        num_refs = timing_results['num_refs']
        for assembler_dir, assembler_results in timing_results.iteritems():
            if num_refs not in comined_results:
                combined_results[num_refs] = {} 
            if assembler_dir not in combined_results[num_refs]:
                combined_results[num_refs][assembler_dir] = [] 
            combined_results[num_refs][assembler_dir].append(assembler_results[plot_key])

    print combined_results

if __name__=="__main__":
    args = interface() 
    reports = load(args.timing_results_pickle) 
    make_timing_plots(reports)

    
