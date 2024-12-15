#!/bin/bash

# Set xtrace to print commands and their arguments as they are executed
set -o xtrace

# Change to the directory where the script is located
cd $(dirname "$0")

# Check if $2 is a compressed file and unzip it if necessary
if [[ $1 == *.gz ]]; then
  gzip -d -f $1
  GENOME_FNA=${1%.gz}  # Remove .gz extension
else
  GENOME_FNA=$1
fi

# Define the path to the genome file
GENOME=${GENOME_FNA%.*}  # Drops the .fna or other extension

# Create an index directory if it does not exist
INDEX_DIR="index"
mkdir -p $INDEX_DIR

# Run HISAT2 build, specifying the output directory for the index files
hisat2-build ${GENOME_FNA} ${INDEX_DIR}/${GENOME}


