#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'

import argparse
from Routines import MatplotlibRoutines

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", action="store", dest="input", required=True,
                    type=lambda s : s.split(","),
                    help="Comma separated list of two input files with data")
parser.add_argument("-d", "--index", action="store", dest="index",
                    type=lambda s: map(int, s.split(",")),
                    help="Zero based indexes of file columns to use. Default: all ")
parser.add_argument("-o", "--output_prefix", action="store", dest="output_prefix",
                    help="Prefix of output files")
parser.add_argument("-s", "--separator", action="store", dest="separator", default=None,
                    help="Separator between values in input file. Default - any space symbol")
parser.add_argument("-l", "--xlabel", action="store", dest="xlabel",
                    help="X label")
parser.add_argument("-y", "--ylabel", action="store", dest="ylabel",
                    help="Y label")


parser.add_argument("-b", "--number_of_bins", action="store", dest="number_of_bins", type=int,
                    help="Number of bins in histogram. Incompatible with -w/--width_of_bins option. Default - 30")

parser.add_argument("-w", "--width_of_bins", action="store", dest="width_of_bins", type=float,
                    help="Width of bins in histogram. Incompatible with -b/--number_of_bins option. Not set by default")
parser.add_argument("-n", "--min_value", action="store", dest="min_length", type=float, default=0,
                    help="Minimum value to show. Default - 1")
parser.add_argument("-x", "--max_value", action="store", dest="max_length", type=float,
                    help="Maximum value to show. Default - length of longest sequence")
parser.add_argument("-g", "--logbase", action="store", dest="logbase", type=int, default=10,
                    help="Logbase to use for log-scaled histograms")
parser.add_argument("-e", "--extensions", action="store", dest="extensions", type=lambda x: x.split(","),
                    default=["png"],
                    help="Comma-separated list of extensions for histogram files. Default: png only")

parser.add_argument("-t", "--title_list", action="store", dest="title_list",
                    help="Comma-separated ist of two title for histograms")

args = parser.parse_args()

if args.index is None:
    args.index = [None for i in range(0, len(args.input))]

MatplotlibRoutines.draw_double_histo_from_file(args.input, args.index, subplot_tuple=(1, 2),
                                               output_prefix=args.output_prefix,
                                               figsize=(5, 10), number_of_bins_list=None, width_of_bins_list=None,
                                               max_threshold_list=None, min_threshold_list=None,
                                               xlabel_list=args.xlabel, ylabel_list=args.ylabel,
                                               title_list=args.title_list, ylogbase_list=None, label_list=None,
                                               extensions=args.extensions, suptitle=None,
                                               separator=args.separator, comments='#')
