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
from numpy import array
from lib.parse import parse_timing_info, dump

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--results-dir', help='Root of test case results dir', required=True)
    args.add_argument('-n', '--notes-file', help='Notes file for the test cases', required=True)
    args.add_argument('-o', '--timing-file', help='Timing results output', default='timing.pkl')
    args = args.parse_args()
    return args

if __name__=="__main__":
    args = interface() 
    reports = parse_timing_info(args.results_dir, args.notes_file)
    dump(reports, args.timing_file)

