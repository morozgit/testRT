FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./service_b ./service_b

CMD ["uvicorn", "service_b.main:app", "--host", "0.0.0.0", "--port", "8002"]
