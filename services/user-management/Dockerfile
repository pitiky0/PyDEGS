FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose environment variables
ENV MYSQL_ROOT_PASSWORD=mysql_password
ENV MYSQL_DATABASE=user_management

CMD ["python3", "./alembic_script.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
