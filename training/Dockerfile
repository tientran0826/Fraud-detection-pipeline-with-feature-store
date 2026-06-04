FROM python:3.10-slim

WORKDIR /app

# Copy all training files
COPY training/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY training/train.py ./train.py
COPY training/api.py ./api.py
COPY training/schemas.py ./schemas.py
COPY training/__init__.py ./__init__.py
COPY training/data/ ./data/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
