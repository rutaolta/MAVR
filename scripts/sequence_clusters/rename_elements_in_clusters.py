#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import argparse

from Routines import SequenceClusterRoutines, FileRoutines


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_cluster_file", action="store", dest="input_cluster_file", required=True,
                    help="Input file with clusters")
parser.add_argument("-s", "--syn_file", action="store", dest="syn_file", required=True,
                    help="File with synonyms to elements")
parser.add_argument("-o", "--output_cluster_file", action="store", dest="output_cluster_file", required=True,
                    help="File to write clusters with renamed elements")
parser.add_argument("-r", "--remove_clusters_with_not_renamed_elements", action="store_true",
                    dest="remove_clusters_with_not_renamed_elements",
                    help="Remove clusters with not renamed elements. Default: false ")

args = parser.parse_args()

SequenceClusterRoutines.rename_elements_in_clusters(args.input_clusters_file, args.syn_file, args.output_clusters_file,
                                                    remove_clusters_with_not_renamed_elements=args.remove_clusters_with_not_renamed_elements)
