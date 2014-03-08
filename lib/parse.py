#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Sam Way", "Rob Knight"] 
__license__ = "GPL"
__version__ = "1.8.0-dev"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

import os
import re
import argparse

def parse_all_reports(results_dir, notes_file):
    """ Parse all QUAST reports to dictionaries """
    results_dirs = [ os.path.join(results_dir, d) for d in os.listdir(results_dir) \
        if os.path.isdir(os.path.join(results_dir, d)) ]
    results_dir_idx = [ int(re.search(r'[0-9]+$', d).group()) for d in results_dirs ]

    params, test_cases = parse_notes(notes_file)
    reference_files = params['REFS']
    max_combine = params['MAX_COMBINE']

    # Initialize reports
    reports = {}
    for ref in reference_files:
        reports[ref] = { i:[] for i in xrange(1, 1+max_combine) }

    for res_dir, res_idx in zip(results_dirs, results_dir_idx):
        included_refs = test_cases[res_idx]
        num_refs = len(included_refs)
        for ref in included_refs:
            temp = res_dir + '/out_quast/' + ref.replace('.fasta', '') + '_quast_output'
            quast_report = parse_quast_report(temp+'/report.tsv')
            reports[ref][num_refs].append(quast_report)

    return reports

def custom_cast(s):
    """ Convert to number/string in that order of preference """
    for cast_func in (int, float, str):
        try:
            return cast_func(s)
        except ValueError:
            pass
    raise BaseException('Could not cast as number/string!')

def parse_notes(notes_file):
    """ Parse NOTES file to dictionaries (one for parameters, the other for test case notes) """
    params = {} 
    test_cases = {} 

    for line in open(notes_file, 'rU'):
        line = line.strip()
        if len(line) < 1:
            continue
        if line[0] == '#':
            pieces = line[1:].split('=')
            if len(pieces) != 2:
                raise ValueError('Invalid parameter specification in NOTES file')
            if line.startswith('#REFS'):
                params['REFS'] = pieces[1].split(',')
            else:
                params[pieces[0].strip()] = custom_cast(pieces[1])
        else: 
            pieces = line.split(':')
            if len(pieces) < 2:
                raise ValueError('Invalid test case notes file')
            test_case_id = int(pieces[0])
            rest = ''.join(pieces[1:])
            rest = rest.replace(' ', '')
            pieces = rest.split(',')
            test_cases[test_case_id] = pieces

    return params, test_cases

