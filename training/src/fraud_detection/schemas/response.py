from pydantic import BaseModel


class TrainResponse(BaseModel):

    run_id: str

    experiment_id: str

    roc_auc: float

    pr_auc: float
