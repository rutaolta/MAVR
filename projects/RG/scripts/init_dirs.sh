#!/usr/bin/env bash

WORKDIR=$1

FASTQ_DIR=${WORKDIR}/fastq/
ANALYSIS_DIR=${WORKDIR}/analysis/
ALIGNMENT_DIR=${WORKDIR}/analysis/alignment/

RAW_READS_DIR=${FASTQ_DIR}/raw/
UNPACKED_READS_DIR=${FASTQ_DIR}/unpacked/
FILTERED_READS_DIR=${FASTQ_DIR}/filtered/




ALIGNMENT_BAM_DIR=${ALIGNMENT_DIR}/bam/
ALIGNMENT_LOG_DIR=${ALIGNMENT_DIR}/log/
ALIGNMENT_TMP_DIR=${ALIGNMENT_DIR}/tmp/

JF_DB_DIR=${ANALYSIS_DIR}/jf/

STAT_DIR=${ANALYSIS_DIR}/stat/
ADAPTERS_STAT_DIR=${STAT_DIR}/adapters/
FASTQC_STAT_DIR=${STAT_DIR}/fastqc/
FILTERING_STAT_DIR=${STAT_DIR}/filtering/
KMER_STAT_DIR=${STAT_DIR}/kmer/

mkkdir ${FASTQ_DIR} ${ANALYSIS_DIR} ${ALIGNMENT_DIR} ${RAW_READS_DIR} ${UNPACKED_READS_DIR}
mkdir ${FILTERED_READS_DIR} ${ALIGNMENT_BAM_DIR} ${ALIGNMENT_LOG_DIR} ${ALIGNMENT_TMP_DIR}
mkdir ${JF_DB_DIR} ${STAT_DIR} ${ADAPTERS_STAT_DIR} ${FASTQC_STAT_DIR} ${FILTERING_STAT_DIR} ${KMER_STAT_DIR}
