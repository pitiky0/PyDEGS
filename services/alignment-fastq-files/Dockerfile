FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y build-essential hisat2 samtools wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz && \
    tar -xvf grch38_genome.tar.gz && \
    rm grch38_genome.tar.gz

WORKDIR /alignement-fastq-files

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run_hisat2.sh
RUN chmod +x indexing_hisat2.sh
CMD ["python", "rabbit_config.py"]