#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import sys
import argparse

from Tools.Clustering import CDhit


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--clustering_file", action="store", dest="clustering_file", required=True,
                    help="Input file with CDHit clusters")
parser.add_argument("-o", "--output", action="store", dest="output", required=True,
                    help="Output fam file")


args = parser.parse_args()


CDhit.convert_clustering_to_fam(args.clustering_file, args.output)
