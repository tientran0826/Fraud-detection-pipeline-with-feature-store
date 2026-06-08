from pydantic import BaseModel, Field


class TrainRequest(BaseModel):

    dataset_path: str

    test_size: float = Field(
        default=0.2,
        ge=0.1,
        le=0.5,
    )

    random_state: int = 42

    n_estimators: int = 500

    max_depth: int = 6

    learning_rate: float = 0.05
