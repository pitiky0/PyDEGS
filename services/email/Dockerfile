FROM python:3.9-slim-buster

WORKDIR /email

COPY ./requirements.txt /email  
RUN pip install --no-cache-dir -r /email/requirements.txt

COPY ./ /email

CMD ["python", "/email/rabbit_config.py"]
