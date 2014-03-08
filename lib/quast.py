#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Sam Way", "Rob Knight"] 
__license__ = "GPL"
__version__ = "1.8.0-dev"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

from .parse import custom_cast

def parse_quast_report(report_file):
    """ Parse quast report to dictionary of dictionaries """ 

    report = open(report_file, 'rU')
    report_dict = {} 

    # Reports start with Assembly\t<assembler_1>\t...\t<assembler_n>
    line = '' 
    while not line.startswith("Assembly"):
        try:
            line = report.readline()
        except: 
            raise ValueError('%s does not appear to be a QUAST report' % (report_file))
    
    assemblers = line.strip().split('\t')[1:]
    num_assemblers = len(assemblers)

    for assembler in assemblers:
        report_dict[assembler] = {} 

    for line in report:
        pieces = line.split('\t')
        if len(pieces) != num_assemblers + 1:
            continue # skip lines without enough arguments
        key = pieces[0].strip()
        for index, assembler in enumerate(assemblers):
            report_dict[assembler][key] = custom_cast(pieces[index+1])

    return report_dict

