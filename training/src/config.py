import os
from dataclasses import dataclass


@dataclass
class Settings:
    mlflow_tracking_uri: str
    experiment_name: str


def get_settings() -> Settings:

    return Settings(
        mlflow_tracking_uri=os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://mlflow:5000",
        ),
        experiment_name=os.getenv(
            "MLFLOW_EXPERIMENT_NAME",
            "fraud-detection",
        ),
    )
