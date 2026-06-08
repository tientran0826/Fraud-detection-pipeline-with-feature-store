FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY infra/compute/data_simulator/producer.py .
COPY training/data ./data

CMD ["python", "-u", "producer.py"]
