import pandas as pd
from fraud_detection.mlflow.logger import log_training_run
from fraud_detection.training.trainer import Trainer


class TrainingService:

    def __init__(self):

        self.trainer = Trainer()

    def train(
        self,
        request,
    ):

        df = pd.read_csv(request.dataset_path)

        (
            model,
            metrics,
            features,
        ) = self.trainer.train(
            df,
            request,
        )

        run_info = log_training_run(
            model,
            metrics,
            features,
        )

        return {
            **metrics,
            **run_info,
        }
