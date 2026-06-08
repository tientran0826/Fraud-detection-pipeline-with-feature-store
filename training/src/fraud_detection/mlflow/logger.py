import mlflow
import mlflow.xgboost


def log_training_run(
    model,
    metrics,
    features,
):

    with mlflow.start_run() as run:

        mlflow.log_metrics(metrics)

        mlflow.log_params({"feature_count": len(features)})

        mlflow.xgboost.log_model(
            model,
            artifact_path="model",
        )

        return {
            "run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
        }
