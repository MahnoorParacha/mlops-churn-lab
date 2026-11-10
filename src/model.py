"""Builds the full sklearn Pipeline: preprocessing + model in ONE object.

Saving preprocessing together with the model means the API applies
exactly the same transformations that were used during training.
"""
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_pipeline(train_params: dict) -> Pipeline:
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocess = ColumnTransformer([
        ("num", numeric, NUMERIC_FEATURES),
        ("cat", categorical, CATEGORICAL_FEATURES),
    ])

    if train_params["model"] == "random_forest":
        clf = RandomForestClassifier(
            n_estimators=train_params["n_estimators"],
            max_depth=train_params["max_depth"],
            min_samples_leaf=train_params["min_samples_leaf"],
            class_weight="balanced",
            random_state=train_params["random_state"],
            n_jobs=-1,
        )
    elif train_params["model"] == "logistic_regression":
        clf = LogisticRegression(
            C=train_params["C"], class_weight="balanced", max_iter=1000
        )
    else:
        raise ValueError(f"Unknown model: {train_params['model']}")

    return Pipeline([("preprocess", preprocess), ("model", clf)])
