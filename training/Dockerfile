FROM python:3.10-slim

WORKDIR /app

# system deps (needed for xgboost build stability)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# install python deps
COPY training/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# default working dir for training script
WORKDIR /app/training

CMD ["python", "train.py"]