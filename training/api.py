from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from schemas import TrainRequest
from train import train_model

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/train")
async def train(request: TrainRequest):

    result = await run_in_threadpool(
        train_model,
        request.dataset_path,
    )

    return result