FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./service_b ./service_b

COPY ./certs/localhost.crt /etc/ssl/certs/service_b.crt
COPY ./certs/localhost.key /etc/ssl/private/service_b.key

CMD ["uvicorn", "service_b.main:app", "--host", "0.0.0.0", "--port", "8002", "--ssl-keyfile", "/etc/ssl/private/service_b.key", "--ssl-certfile", "/etc/ssl/certs/service_b.crt"]
