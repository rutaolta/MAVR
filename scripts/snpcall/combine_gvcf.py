#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import argparse

from Tools.GATK import CatVariants


parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", action="store", dest="output", required=True,
                    help="Output vcf file")
parser.add_argument("-r", "--reference", action="store", dest="reference", required=True,
                    help="Fasta with reference genome")
parser.add_argument("-g", "--gatk_directory", action="store", dest="gatk_dir", default="",
                    help="Directory with GATK jar")
parser.add_argument("-i", "--input_gvcf_list", action="store", dest="input_gvcf_list", type=lambda s: s.split(","),
                    help="Comma-separated list of gvcf files to combine",  required=True,)
parser.add_argument("-s", "--sorted", action="store_true", dest="sorted", default=False,
                    help="Input gvcf are coordinate sorted. Default: False")
args = parser.parse_args()

CatVariants.jar_path = args.gatk_dir

CatVariants.combine_gvcf(args.reference, args.input_gvcf_list, args.output, input_is_sorted=args.sorted)
