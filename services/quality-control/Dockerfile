FROM python:3.9-slim-buster

WORKDIR /quality-control

RUN apt-get update && apt-get install -y fastqc

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "rabbit_config.py"]