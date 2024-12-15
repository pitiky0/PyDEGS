FROM python:3.9-slim-buster

WORKDIR /filtering-fastq-files

## Install Trimmomatic
RUN     cd /filtering-fastq-files \
&&      apt-get update \
&&      apt-get install -y openjdk-11-jre-headless \
&&      apt-get install -y wget unzip gcc libz-dev \
&&      wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip \
&&      unzip Trimmomatic-0.39.zip \
&&      cd / \
&&      apt autoremove -y wget unzip \
&&      rm -rf Trimmomatic-0.39.zip \
&&      rm -rf /tmp/* \
&&      rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "rabbit_config.py"]