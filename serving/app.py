from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from feast import FeatureStore
import os

app = FastAPI(
    title="Fraud Detection Serving API",
    description="API to get fraud predictions based on features stored in Feast.",
    version="1.0"
)

REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../feature_repo"))
store = FeatureStore(repo_path=REPO_PATH)

class PredictionRequest(BaseModel):
    user_id: int

def mock_fraud_model(click_count: int) -> dict:
    is_fraud = False
    fraud_probability = 0.05
    
    if click_count > 100:
        is_fraud = True
        fraud_probability = min(0.1 + (click_count * 0.008), 0.95)
    elif click_count > 50:
        fraud_probability = 0.35
        
    return {
        "is_fraud": is_fraud,
        "fraud_probability": round(fraud_probability, 2),
        "verdict": "CRITICAL_ALERT" if is_fraud else "NORMAL_TRAFFIC"
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        print("REQUEST USER:", request.user_id)
        
        feature_vector = store.get_online_features(
            features=[
                "user_click_features:click_count"
            ],
            entity_rows=[{"user_id": request.user_id}]
        ).to_dict()
        
        print("FEATURE VECTOR:", feature_vector)

        current_click_count = feature_vector.get(
            "click_count",
            [None]
        )[0]
        if current_click_count is None:
            raise HTTPException(
                status_code=404,
                detail=f"User ID {request.user_id} does not have click count data available."
            )

        prediction_result = mock_fraud_model(current_click_count)

        return {
            "user_id": request.user_id,
            "features_retrieved": {
                "click_count": current_click_count
            },
            "prediction": prediction_result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
def health_check():
    return {"status": "healthy"}