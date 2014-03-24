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
from lib.plot_helpers import color_bp

def interface():
    args = argparse.ArgumentParser() 
    args.add_argument('-i', '--results-pickle', help='Results pickle', required=True)
    args.add_argument('-o', '--output-prefix', help='Prefix for generated files', required=True)
    args.add_argument('-s', '--output-suffix', help='Suffix/filetype for output files', \
        default='.pdf')
    args = args.parse_args()
    return args

def make_plots(reports, output_name, references=None, assemblers=None):

    key = 'N50' #'# misassemblies' #'Genome fraction (%)'
    normalize = False 
    normalize_by = 'Reference length'
    plot_bar = False
    legend_loc='upper left'
    if references is None:
        references = reports.keys()
    if len(references) == 1:
        ref_title = references[0]
    else:
        ref_title = "multiple references"
    mixtures = reports[references[0]].keys()
    if assemblers is None:
        assemblers = reports[references[0]][1][0].keys() 
    num_assemblers = len(assemblers)
    width = 0.2

    positions = range(1, num_assemblers+1)

    fig = plt.figure()
    ax = plt.axes()
    colors = brewer2mpl.get_map('Set2', 'Qualitative', num_assemblers).mpl_colors
    plt.hold(True)
    assembler_output = {} 

    for assembler in assemblers:
        value_dict = { i:[] for i in mixtures } 
        for ref in references:
            for m in mixtures:
                for report in reports[ref][m]:
                    if normalize:
                        value_dict[m].append(float(report[assembler][key]) / \
                            report[assembler][normalize_by])
                    else:
                        value_dict[m].append(report[assembler][key])
        assembler_output[assembler] = value_dict

    base_range = array(range(1, len(mixtures)+1))
    bar_handles = []
    for index, assembler in enumerate(assemblers):
        ind = base_range + index*width
        means = []
        mins = []
        maxs = []
        stds = []
        for m in mixtures:
            data = array(assembler_output[assembler][m])
            means.append(data.mean())
            stds.append(data.std())
            mins.append(means[-1] - data.min())
            maxs.append(data.max() - means[-1])
        bars = ax.bar(ind, means, width, color=colors[index], ecolor='k', \
            yerr=(mins,maxs), alpha=0.9)
        bar_handles.append(bars)

    ax.legend( tuple(bar_handles), assemblers, loc=legend_loc)
    ax.set_xticks(base_range + (num_assemblers*width/2))
    ax.set_xticklabels( ([str(m) for m in mixtures ]) )
    plt.title(key + ' for ' + ref_title)
    plt.ylabel(key)
    plt.xlabel('Co-assembly number')
    if plot_bar: 
        plt.savefig(output_name)
    #plt.show()
    plt.hold(False)

    fig = plt.figure()
    ax = plt.axes()
    plt.hold(True)
    # For box plots:
    xticks = []
    for m in mixtures:
        # positions groups by assembler
        positions = range(((m-1)+(m)*num_assemblers)-num_assemblers+1, ((m-1)+(m)*num_assemblers)+1)
        xticks.append(array(positions).mean())
        data = [ assembler_output[assembler][m] for assembler in assemblers ]
        bp = ax.boxplot(data, positions=positions, widths=0.6)
        color_bp(bp, colors)
    ax.set_xticks(xticks)
    ax.set_xticklabels( ([str(m) for m in mixtures ]) )
    plt.xlim(0,max(positions)+2)

    # Fake lines to get a legend
    fake = []
    for i in xrange(num_assemblers):
        h, = plt.plot([0,0], [0,0.01], linewidth=4, color=colors[i])
        fake.append(h)
    plt.legend(fake, assemblers, loc=legend_loc)
    for f in fake:
        f.set_visible(False)

    plt.title(key + ' for ' + ref_title)
    plt.ylabel(key)
    plt.xlabel('Co-assembly number')
    #plt.show()
    plt.hold(False)
    if not plot_bar:
        plt.savefig(output_name)

if __name__=="__main__":
    args = interface() 
    reports = load(args.results_pickle) 
    for ref in reports.keys():  
        output_name = args.output_prefix + ref + args.output_suffix
        make_plots(reports, output_name, references=[ref])

    
