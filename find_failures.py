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
from lib.parse import print_failed_reports

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--results-dir', help='Root of test case results dir', required=True)
    args.add_argument('-n', '--notes-file', help='Notes file for the test cases', required=True)
    args = args.parse_args()
    return args

if __name__=="__main__":
    args = interface() 
    print_failed_reports(args.results_dir, args.notes_file)
   
