import json
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from feast import FeatureStore

def push_to_feast(record_str):
    print("RECEIVED:", record_str)
    store = FeatureStore(repo_path="/opt/flink/usrlib/feature_repo")
    data = json.loads(record_str)
    
    import pandas as pd
    from datetime import datetime, timezone
    
    now = datetime.now(timezone.utc)
    
    event_df = pd.DataFrame([{
        "user_id": int(data["user_id"]),
        "click_count": int(data["click_count"]),
        "event_timestamp": now,
        "created_timestamp": now,
    }])
    
    store.push("streaming_source", event_df)
    print(f"🌟 Pushed to Feast: {data}")

def run_flink_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    
    ds = env.from_collection(
        collection=[
            '{"user_id": 99901, "click_count": 12}',
            '{"user_id": 99902, "click_count": 89}'
        ],
        type_info=Types.STRING()
    )
    
    ds.map(push_to_feast)
    env.execute("Flink-Feast-Push-Job")

if __name__ == "__main__":
    run_flink_pipeline()