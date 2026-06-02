# Fraud Detection Pipeline with Feature Store

An end-to-end real-time fraud detection pipeline built using Apache Flink, Feast Feature Store, Redis, and FastAPI. The project demonstrates how streaming events can be transformed into online features, stored in a feature store, and served for low-latency fraud prediction.

## Architecture

```text
Event Stream
      │
      ▼
 Apache Flink
      │
      ▼
 Feast PushSource
      │
      ▼
 Redis Online Store
      │
      ▼
 FastAPI Serving Layer
      │
      ▼
 Fraud Prediction API
```

## Features

* Real-time feature ingestion using Apache Flink
* Online feature storage with Feast and Redis
* Low-latency feature retrieval for inference
* FastAPI serving endpoint
* Mock fraud detection model for demonstration
* Docker Compose deployment

## Tech Stack

| Component         | Technology   |
| ----------------- | ------------ |
| Stream Processing | Apache Flink |
| Feature Store     | Feast        |
| Online Store      | Redis        |
| API Serving       | FastAPI      |
| Containerization  | Docker       |
| Language          | Python 3.10  |

## Project Structure

```text
.
├── feature_repo/
│   ├── feature_store.yaml
│   ├── features/
│   └── data/
│
├── infra/
│   └── compute/
│       └── flink/
│           └── flink_job.py
│
├── serving/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Start Infrastructure

```bash
docker compose up -d
```

Services:

* Flink JobManager
* Flink TaskManager
* Redis
* FastAPI Serving

### 2. Apply Feast Configuration

```bash
cd feature_repo

feast apply
```

### 3. Run Flink Job

```bash
docker compose exec jobmanager \
flink run -py /opt/flink/usrlib/infra/compute/flink/flink_job.py
```

Example events:

```json
{
  "user_id": 99901,
  "click_count": 12
}
```

```json
{
  "user_id": 99902,
  "click_count": 89
}
```

The Flink job pushes feature values into Feast through a PushSource and stores them in Redis.

## API Usage

### Health Check

```bash
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Fraud Prediction

```bash
POST /predict
```

Request:

```json
{
  "user_id": 99901
}
```

Response:

```json
{
  "user_id": 99901,
  "features_retrieved": {
    "click_count": 12
  },
  "prediction": {
    "is_fraud": false,
    "fraud_probability": 0.05,
    "verdict": "NORMAL_TRAFFIC"
  }
}
```

## Feast Feature Definition

```python
user_click_feature_view = FeatureView(
    name="user_click_features",
    entities=[user],
    schema=[
        Field(name="click_count", dtype=Int64),
    ],
    source=streaming_source,
    online=True,
)
```

## Learning Objectives

This project demonstrates:

* Real-time feature engineering
* Streaming ML architectures
* Feature Store concepts
* Online feature serving
* Low-latency inference patterns
* MLOps fundamentals

## Future Improvements

* Kafka event ingestion
* Real fraud detection model (XGBoost/LightGBM)
* Batch feature backfills
* Monitoring and observability
* CI/CD pipelines
* Feature validation and drift detection

## License

MIT License
