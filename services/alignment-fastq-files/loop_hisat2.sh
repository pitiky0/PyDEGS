#!/bin/bash

set -o xtrace

# Define the directory containing your FASTQ files
FASTQ_DIR="fastq-files"

# Loop over each pair of FASTQ files
for fq1 in ${FASTQ_DIR}/*1.*.gz; do
  fq2=$(echo ${fq1} | sed 's/_1./_2./g')
  bash run_hisat2.sh ${fq1} ${fq2}
done &> hisat2_1.log
