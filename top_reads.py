from Bio import SeqIO
from collections import Counter
import gzip

def count_reads(input_file, top_n=10):
    """Count the occurrences of each read in the FASTQ file."""
    read_counter = Counter()
    
    with gzip.open(input_file, "rt") if input_file.endswith(".gz") else open(input_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            read_counter[str(record.seq)] += 1

    return read_counter.most_common(top_n)

def main(input_file, top_n=10):
    top_reads = count_reads(input_file, top_n)
    
    print(f"Top {top_n} reads:")
    for i, (read, count) in enumerate(top_reads, 1):
        print(f"{i}. Read: {read}, Count: {count}")

if __name__ == "__main__":
    input_file = 'C:\\Users\\Ayoub\\Downloads\\fastq files\\13681.fastq.gz'  # Replace with the path to your FASTQ file
    top_n = 10  # Number of top reads to return
    main(input_file, top_n)
