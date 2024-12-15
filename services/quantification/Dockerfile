FROM python:3.9-slim-buster

WORKDIR /quantification

RUN apt-get update \
    && apt-get install -y subread wget \
    && rm -rf /var/lib/apt/lists/*

RUN cd /quantification \
    && wget https://ftp.ensembl.org/pub/release-112/gtf/homo_sapiens/Homo_sapiens.GRCh38.112.gtf.gz \
    && gunzip Homo_sapiens.GRCh38.112.gtf.gz \
    && rm -rf Homo_sapiens.GRCh38.112.gtf.gz

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "quantification_features.py"]