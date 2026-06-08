from xgboost import XGBClassifier


def create_model(
    scale_pos_weight: float,
    n_estimators: int,
    max_depth: int,
    learning_rate: float,
):

    return XGBClassifier(
        objective="binary:logistic",
        eval_metric="aucpr",
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1,
    )
