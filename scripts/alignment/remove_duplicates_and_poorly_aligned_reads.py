#!/usr/bin/env python
__author__ = 'mahajrod'

import argparse

from Tools.Samtools import SamtoolsV1

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_bam", action="store", dest="input_bam",
                    help="Input bam. Default: stdout")
parser.add_argument("-q", "--min_map_quality", action="store", dest="min_map_quality", default=20, type=int,
                    help="Minimum mapping quality to retain read")
parser.add_argument("-o", "--output_bam", action="store", dest="output_bam",
                    help="Output bam. Default: stdout")

args = parser.parse_args()

SamtoolsV1.remove_duplicates_and_poorly_aligned_reads(input_bam=args.input_bam,
                                                      output_bam=args.output_bam,
                                                      min_mapping_quality=args.min_map_quality)
