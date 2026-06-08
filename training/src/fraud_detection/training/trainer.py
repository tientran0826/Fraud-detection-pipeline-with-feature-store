from fraud_detection.features.engineering import build_features
from fraud_detection.models.xgboost_factory import create_model
from fraud_detection.schemas.creditcard import CreditCardSchema
from fraud_detection.utils.schema_validator import validate_columns
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split


class Trainer:

    def train(
        self,
        df,
        request,
    ):

        validate_columns(
            df,
            CreditCardSchema.REQUIRED_COLUMNS,
        )

        df = build_features(df)

        X = df.drop(columns=[CreditCardSchema.TARGET])

        y = df[CreditCardSchema.TARGET]

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = train_test_split(
            X,
            y,
            test_size=request.test_size,
            random_state=request.random_state,
            stratify=y,
        )

        fraud_count = y_train.sum()

        normal_count = len(y_train) - fraud_count

        scale_pos_weight = normal_count / fraud_count

        model = create_model(
            scale_pos_weight=scale_pos_weight,
            n_estimators=request.n_estimators,
            max_depth=request.max_depth,
            learning_rate=request.learning_rate,
        )

        model.fit(
            X_train,
            y_train,
        )

        pred = model.predict_proba(X_test)[:, 1]

        metrics = {
            "roc_auc": float(
                roc_auc_score(
                    y_test,
                    pred,
                )
            ),
            "pr_auc": float(
                average_precision_score(
                    y_test,
                    pred,
                )
            ),
        }

        return (
            model,
            metrics,
            X.columns.tolist(),
        )
