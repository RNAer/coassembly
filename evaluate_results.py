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
from lib.quast import parse_quast_report
from lib.parse import parse_notes, parse_all_reports
import matplotlib.pyplot as plt

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--results-dir', help='Root of test case results dir', required=True)
    args.add_argument('-n', '--notes-file', help='Notes file for the test cases', required=True)
    args = args.parse_args()
    return args

def plot_genome_percentage(reports, output_name='gen_per.pdf'):

    key = 'Genome fraction (%)'
    references = reports.keys()
    mixtures = reports[references[0]].keys()
    assemblers = reports[references[0]][1][0].keys() 
    num_assemblers = len(assemblers)
    width = 0.1

    positions = range(1, num_assemblers+1)

    fig = plt.figure()
    ax = plt.axes()
    colors = ['c', 'm', 'y', 'k']
    plt.hold(True)
    assembler_output = {} 

    for assembler in assemblers:
        value_dict = { i:[] for i in mixtures } 
        for ref in references:
            for m in mixtures:
                for report in reports[ref][m]:
                    value_dict[m].append(report[assembler][key])
        assembler_output[assembler] = value_dict

    base_range = array(range(1, len(mixtures)+1))
    for index, assembler in enumerate(assemblers):
        ind = base_range + index*width
        means = []
        stds = []
        for m in mixtures:
            data = array(assembler_output[assembler][m])
            means.append(data.mean())
            stds.append(data.std())
        rects = ax.bar(ind, means, width, color=colors[index], yerr=stds)
    
    """
    for m in mixtures:
        # positions groups by assembler
        positions = range(((m-1)+(m)*num_assemblers)-num_assemblers+1, ((m-1)+(m)*num_assemblers)+1)
        data = [ assembler_output[assembler][m] for assembler in assemblers ]
        bp = plt.boxplot(data, positions=positions, widths = 0.6)
    """

    plt.hold(False)
    #plt.savefig(output_name)
    plt.show()


if __name__=="__main__":
    args = interface() 
    reports = parse_all_reports(args.results_dir, args.notes_file)
    plot_genome_percentage(reports)
   

