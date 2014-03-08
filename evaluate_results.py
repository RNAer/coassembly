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
from lib.quast import parse_quast_report
from lib.parse import parse_notes, parse_all_reports

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--results-dir', help='Root of test case results dir', required=True)
    args.add_argument('-n', '--notes-file', help='Notes file for the test cases', required=True)
    args = args.parse_args()
    return args

def plot_genome_percentage(reports):

    references = reports.keys()
    mixtures = reports[references[0]].keys()
    assemblers = reports[references[0]][1][0].keys() 

    print references
    print mixtures
    print assemblers 
    

if __name__=="__main__":
    args = interface() 
    reports = parse_all_reports(args.results_dir, args.notes_file)
    plot_genome_percentage(reports)
   

