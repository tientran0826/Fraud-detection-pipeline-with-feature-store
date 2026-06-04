from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, PushSource, ValueType
from feast.types import Int64

user = Entity(name="user_id", value_type=ValueType.INT64, description="User ID")

dummy_batch_source = FileSource(
    name="dummy_batch_source",
    path="data/dummy_history.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

streaming_source = PushSource(name="streaming_source", batch_source=dummy_batch_source)

user_click_feature_view = FeatureView(
    name="user_click_features",
    entities=[user],
    schema=[
        Field(name="click_count", dtype=Int64),
    ],
    online=True,
    source=streaming_source,
    ttl=timedelta(days=1),
)
