#!/usr/bin/env bash
#SBATCH --array=1-38%5
#SBATCH -n 5
#SBATCH --time=100:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=8096       # Minimum memory required per CPU (in megabytes)
#SBATCH --job-name=filtering_raw
#SBATCH --error=/work/pavlov/okochenova/job_reports/RUN7/mating_type_detection_RUN7.%A_%a.err
#SBATCH --output=/work/pavlov/okochenova/job_reports/RUN7/mating_type_detection_RUN7.%A_%a.out

module load compiler/gcc/4.8 python/2.7 samtools/0.1 bowtie/2.2 sage/6.3 zlib/1.2

source /work/pavlov/okochenova/profile
echo ${PYTHONPATH}
OKOCHENOVA_DIR="/work/pavlov/okochenova/"
SOFT_DIR=${OKOCHENOVA_DIR}"soft/"
WORKDIR=${OKOCHENOVA_DIR}"/mating_type_detection/"

BOWTIE2_INDEX=${WORKDIR}"index/mating_rel_seqs"

MAVR_SCRIPTS_DIR=${SOFT_DIR}"/MAVR/scripts/"
RESTORE_PAIRS_SCRIPT=${MAVR_SCRIPTS_DIR}"filter/restore_pairs.py"
MAP_SCRIPT=${MAVR_SCRIPTS_DIR}"alignment/map_reads.py"

EXTRACTOR_BIN=${SOFT_DIR}"Cookiecutter/src/extract"
FRAGMENTS_FILE=${WORKDIR}"kmer/mating_rel_seqs_with_rev_com_33_mer.kmer"
SAMPLES_DIR=${OKOCHENOVA_DIR}"fastq/RUN7/"



SAMPLES=(N085-LAN210-Can-PmCDA1-NA-RUN7-D1 N086-LAN210-Can-PmCDA1-NA-RUN7-D1 N087-LAN210-Can-PmCDA1-NA-RUN7-D1 N088-LAN210-Can-PmCDA1-NA-RUN7-D1 N089-LAN210-Can-PmCDA1-NA-RUN7-D1 N090-LAN210-Can-PmCDA1-NA-RUN7-D1 N091-LAN210-Can-PmCDA1-NA-RUN7-D3 N092-LAN210-Can-PmCDA1-NA-RUN7-D6 N093-LAN210-Can-PmCDA1-NA-RUN7-D6 N094-LAN210-Can-PmCDA1-NA-RUN7-D6 N095-LAN210-Can-PmCDA1-NA-RUN7-D6 N096-LAN210-Can-PmCDA1-NA-RUN7-D6 N097-LAN210-Can-AID-NA-RUN7-D1 N098-LAN210-Can-AID-NA-RUN7-D1 N100-LAN210-Can-AID-NA-RUN7-D3 N101-LAN210-Can-AID-NA-RUN7-D3 N102-LAN210-Can-AID-NA-RUN7-D3 N103-LAN210-Can-AID-NA-RUN7-D6 N104-LAN210-Can-AID-NA-RUN7-D6 N105-LAN210-Can-AID-NA-RUN7-D6 N106-LAN210-Can-AID-NA-RUN7-D6 N107-LAN210-Can-A1-NA-RUN7-D1 N108-LAN210-Can-A1-NA-RUN7-D1 N109-LAN210-Can-A1-NA-RUN7-D1 N110-LAN210-Can-A1-NA-RUN7-D1 N111-LAN210-Can-A1-NA-RUN7-D1 N112-LAN210-Can-A1-NA-RUN7-D1 N113-LAN210-Can-A1-NA-RUN7-D3 N114-LAN210-Can-A1-NA-RUN7-D3 N115-LAN210-Can-A1-NA-RUN7-D3 N116-LAN210-Can-A1-NA-RUN7-D3 N117-LAN210-Can-A1-NA-RUN7-D3 N118-LAN210-Can-A1-NA-RUN7-D3 N120-LAN210-Can-A1-NA-RUN7-D6 N121-LAN210-Can-A1-NA-RUN7-D6 N122-LAN210-Can-A1-NA-RUN7-D6 N123-LAN210-Can-A1-NA-RUN7-D6 N124-LAN210-Can-A1-NA-RUN7-D6)

cd ${WORKDIR}

let "SAMPLE_INDEX=${SLURM_ARRAY_TASK_ID}-1"
CURRENT_SAMPLE=${SAMPLES[${SAMPLE_INDEX}]}

READS_DIR=${SAMPLES_DIR}${CURRENT_SAMPLE}"/filtered_ns/filtered/trimmed/"

LEFT_READS_FILE=${READS_DIR}${CURRENT_SAMPLE}"_1.ok_val_1.fq"
RIGHT_READS_FILE=${READS_DIR}${CURRENT_SAMPLE}"_2.ok_val_2.fq"

echo "Left reads file ${LEFT_READS_FILE}"
echo "Right reads file ${RIGHT_READS_FILE}"
mkdir -p ${CURRENT_SAMPLE}
cd ${CURRENT_SAMPLE}
echo ${CURRENT_SAMPLE}
mkdir -p both_reads
mkdir -p all_reads

#${EXTRACTOR_BIN} --fragments ${FRAGMENTS_FILE} -o ./ -1 ${LEFT_READS_FILE} -2 ${RIGHT_READS_FILE}

EXTRACTED_READS_FILE_LEFT=${CURRENT_SAMPLE}"_1.ok_val_1.filtered.fastq"
EXTRACTED_READS_FILE_LEFT_SE=${CURRENT_SAMPLE}"_1.ok_val_1.se.fastq"
EXTRACTED_READS_FILE_RIGHT=${CURRENT_SAMPLE}"_2.ok_val_2.filtered.fastq"
EXTRACTED_READS_FILE_RIGHT_SE=${CURRENT_SAMPLE}"_2.ok_val_2.se.fastq"

BOTH_PREFIX=./both_reads/${CURRENT_SAMPLE}"_both"
ALL_PREFIX=./all_reads/${CURRENT_SAMPLE}"_all"

${RESTORE_PAIRS_SCRIPT} -l ${EXTRACTED_READS_FILE_LEFT} -r ${EXTRACTED_READS_FILE_RIGHT} \
                        -o ${BOTH_PREFIX}
${RESTORE_PAIRS_SCRIPT} -l ${EXTRACTED_READS_FILE_LEFT},${EXTRACTED_READS_FILE_LEFT_SE} \
                        -r ${EXTRACTED_READS_FILE_RIGHT},${EXTRACTED_READS_FILE_RIGHT_SE} \
                        -o ${ALL_PREFIX}

${MAP_SCRIPT} -i ${BOWTIE2_INDEX} -t 4 -r ${BOTH_PREFIX}"_1.fastq" -l ${BOTH_PREFIX}"_2.fastq" -p ${BOTH_PREFIX} -g -y ${BOTH_PREFIX}"_coverage.bed"
${MAP_SCRIPT} -i ${BOWTIE2_INDEX} -t 4 -r ${ALL_PREFIX}"_1.fastq" -l ${ALL_PREFIX}"_2.fastq" -p ${ALL_PREFIX} -g -y ${ALL_PREFIX}"_coverage.bed"