import os

import mlflow
import mlflow.xgboost
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

load_dotenv()


def train_model(dataset_path: str) -> dict:
    """
    Train XGBoost model and log everything to MLflow.

    Returns
    -------
    dict
        Training metadata.
    """

    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    experiment_name = os.getenv(
        "MLFLOW_EXPERIMENT_NAME",
        "fraud-detection",
    )

    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name)

    df = pd.read_csv(dataset_path)

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    with mlflow.start_run() as run:

        model = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            eval_metric="aucpr",
            random_state=42,
        )

        model.fit(X_train, y_train)

        predictions = model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(
            y_test,
            predictions,
        )

        mlflow.log_params(
            {
                "model": "xgboost",
                "n_estimators": 300,
                "max_depth": 6,
                "learning_rate": 0.05,
                "eval_metric": "aucpr",
            }
        )

        mlflow.log_metric("auc", auc)

        mlflow.xgboost.log_model(
            xgb_model=model,
            artifact_path="model",
        )

        result = {
            "run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "auc": float(auc),
        }

        print(result)

        return result
