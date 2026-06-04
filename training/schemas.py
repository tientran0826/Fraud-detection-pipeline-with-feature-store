from pydantic import BaseModel


class TrainRequest(BaseModel):
    dataset_path: str


class TrainResponse(BaseModel):
    run_id: str
    auc: float