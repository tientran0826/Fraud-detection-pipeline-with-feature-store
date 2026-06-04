FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY infra/orchestration/prefect/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY infra/orchestration/prefect .

CMD ["sleep", "infinity"]
