import json
import logging
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction, RuntimeContext
from feast import FeatureStore
import pandas as pd
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeastPushFunction(MapFunction):
    """MapFunction to push events from Kafka to Feast feature store"""
    
    def __init__(self):
        self.store = None
        self.count = 0
    
    def open(self, runtime_context: RuntimeContext):
        """Initialize Feast store connection"""
        try:
            self.store = FeatureStore(repo_path="/opt/flink/usrlib/feature_repo")
            logger.info("Feast FeatureStore initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Feast: {e}")
            raise
    
    def map(self, record_str):
        """Process each Kafka message and push to Feast"""
        try:
            data = json.loads(record_str)
            logger.info(f"Processing Kafka event: {data}")
            
            now = datetime.now(timezone.utc)
            
            # Create DataFrame matching the feature view schema
            event_df = pd.DataFrame([{
                "user_id": int(data["user_id"]),
                "click_count": int(data["click_count"]),
                "event_timestamp": now,
                "created_timestamp": now,
            }])
            
            # Push to Feast
            self.store.push("streaming_source", event_df)
            self.count += 1
            
            logger.info(f"Pushed to Feast [{self.count}]: user_id={data['user_id']}, "
                       f"clicks={data['click_count']}")
            
            return f"Success: {data['user_id']}"
            
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return f"Error: {str(e)}"

def run_flink_pipeline():
    """Set up and run Flink stream processing pipeline"""
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    
    try:
        from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
        from pyflink.common.serialization import SimpleStringSchema
        from pyflink.common.typeinfo import Types
        
        env.add_jars("file:///opt/flink/usrlib/flink-sql-connector-kafka-3.1.0-1.18.jar")

        properties = {
            'bootstrap.servers': 'kafka:29092',
            'group.id': 'flink-fraud-detection',
            'auto.offset.reset': 'latest'
        }
        
        logger.info("Connecting to Kafka topic 'user-events'...")
        
        kafka_consumer = FlinkKafkaConsumer(
            topics='user-events',
            deserialization_schema=SimpleStringSchema(),
            properties=properties
        )
        
        ds = env.add_source(kafka_consumer)
        
        ds.map(FeastPushFunction()).print()
        
        logger.info("Starting Flink-Kafka-Feast-Pipeline Streaming Job...")
        env.execute("Flink-Kafka-Feast-Pipeline")
        
    except Exception as e:
        logger.error(f"Flink pipeline error: {e}")
        raise

if __name__ == "__main__":
    run_flink_pipeline()