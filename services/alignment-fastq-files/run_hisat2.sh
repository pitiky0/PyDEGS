#!/bin/bash

set -o xtrace

# set the reference index:
GENOME="$1"

# make an output directory to store the output aligned files
OUTDIR="$2"
[[ -d ${OUTDIR} ]] || mkdir -p ${OUTDIR}  # If output directory doesn't exist, create it

R1_FQ="$3"  
R2_FQ="$4"  

# check if $4 provided, if not, set R2_FQ to empty string
if [ -z "$4" ]; then
  R2_FQ=""
fi

OUTFILE=$(basename ${R1_FQ} | cut -f 2 -d ".")

# check if R2_FQ is empty
if [ -z "$R2_FQ" ]; then
  hisat2 \
    -x ${GENOME} \
    -U ${R1_FQ} \
    -S ${OUTDIR}/${OUTFILE}.sam &> ${OUTDIR}/${OUTFILE}.log
else
  hisat2 \
    -x ${GENOME} \
    -1 ${R1_FQ} \
    -2 ${R2_FQ} \
    -S ${OUTDIR}/${OUTFILE}.sam &> ${OUTDIR}/${OUTFILE}.log
fi

samtools view --threads ${p} -bS -o ${OUTDIR}/${OUTFILE}.bam ${OUTDIR}/${OUTFILE}.sam

rm ${OUTDIR}/${OUTFILE}.sam
