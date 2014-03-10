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
    args.add_argument('-i', '--timing-results-pickle', help='Timing results pickle', required=True)
    args = args.parse_args()
    return args

def make_timing_plots(timing_dict):
    plot_key = 'mem'
    combined_results = {} 

    for res_idx, timing_results in timing_dict.iteritems():
        num_refs = timing_results['num_refs']
        for assembler_dir, assembler_results in timing_results.iteritems():
            if assembler_dir == 'num_refs': continue
            if num_refs not in combined_results:
                combined_results[num_refs] = {} 
            if assembler_dir not in combined_results[num_refs]:
                combined_results[num_refs][assembler_dir] = [] 
            combined_results[num_refs][assembler_dir].append(assembler_results[plot_key])

    mixtures = combined_results.keys()
    assemblers = combined_results[mixtures[-1]].keys()
    num_assemblers = len(assemblers)
    colors = brewer2mpl.get_map('Set2', 'Qualitative', num_assemblers).mpl_colors
    xticks = []

    ax = plt.axes()
    plt.hold(True)
    
    for m in mixtures:
        positions = range(((m-1)+(m)*num_assemblers)-num_assemblers+1, ((m-1)+(m)*num_assemblers)+1)
        xticks.append(array(positions).mean())
        data = [ combined_results[m][assembler] for assembler in assemblers ]
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
    plt.legend(fake, assemblers, loc='upper left')
    for f in fake:
        f.set_visible(False)

    plt.ylabel(plot_key)
    plt.xlabel('Co-assembly number')
    plt.show()
    plt.hold(False)

if __name__=="__main__":
    args = interface() 
    reports = load(args.timing_results_pickle) 
    make_timing_plots(reports)

    
