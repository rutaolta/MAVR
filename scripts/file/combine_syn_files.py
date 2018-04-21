#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import sys
import argparse

from Routines import FileRoutines


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", action="store", dest="input", required=True,
                    type=lambda s:s.split(","),
                    help="Comma-separated list of syn files")
parser.add_argument("-o", "--output", action="store", dest="output", default=sys.stdout,
                    help="Output merged syn file")
parser.add_argument("-k", "--key_column", action="store", dest="key_column", default=0, type=int,
                    help="Column to be used as key(0-based). Default: 0")
parser.add_argument("-v", "--value_column", action="store", dest="value_column", default=1, type=int,
                    help="Column to be used as value(0-based). Default: 1")
parser.add_argument("-s", "--separator", action="store", dest="separator", default="\t",
                    help="Separator used in input file. Default: TAB")
parser.add_argument("-e", "--value_separator", action="store", dest="value_separator", default=",",
                    help="Value separator in input file. Default: ,")

args = parser.parse_args()

FileRoutines.combine_syn_dicts_from_file(args.input, args.output,
                                         key_index=args.key_colum,
                                         value_index=args.value_column,
                                         separator=args.separator,
                                         values_separator=args.value_separator)