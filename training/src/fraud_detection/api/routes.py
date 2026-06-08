from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from fraud_detection.schemas.request import TrainRequest
from fraud_detection.schemas.response import TrainResponse
from fraud_detection.services.training_service import TrainingService

router = APIRouter()

training_service = TrainingService()


@router.get("/health")
def health():

    return {"status": "ok"}


@router.post(
    "/train",
    response_model=TrainResponse,
)
async def train(
    request: TrainRequest,
):

    return await run_in_threadpool(
        training_service.train,
        request,
    )
