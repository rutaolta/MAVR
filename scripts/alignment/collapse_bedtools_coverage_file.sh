#!/usr/bin/env bash

awk -F'\t' 'BEGIN {SCAF=""; LEN=""; COV=""} {if ($1 != SCAF) {printf "%s\t%s\t%s\n",SCAF,LEN, COV; SCAF=$1; LEN=$2; COV=$3} else {LEN=$2; COV=COV","$3}}' $1
