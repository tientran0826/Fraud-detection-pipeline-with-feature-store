import requests
from prefect import flow, get_run_logger, task


@task
def trigger_training():
    logger = get_run_logger()
    response = requests.post(
        "http://training:8001/train",
        json={"dataset_path": "data/creditcard.csv"},
        timeout=3600,
    )

    logger.info(f"Status: {response.status_code}")
    logger.info(f"BODY: {response.text}")

    response.raise_for_status()

    return response.json()


@flow(name="fraud-training")
def training_flow():

    result = trigger_training()
