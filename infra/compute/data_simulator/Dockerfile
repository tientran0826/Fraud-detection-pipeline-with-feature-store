FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY infra/compute/data_simulator/producer.py .

CMD ["python", "producer.py"]
