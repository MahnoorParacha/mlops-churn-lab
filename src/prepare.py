"""Stage 2: basic cleaning with pandas, then train/test split."""
import os

import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import FEATURES, PROCESSED_DIR, TARGET, load_params


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw churn table."""
    df = df.copy()
    df = df.drop_duplicates()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges"])
    df[TARGET] = df[TARGET].map({"Yes": 1, "No": 0})
    return df[FEATURES + [TARGET]]
    
def main():
    params = load_params()["data"]
    raw = pd.read_csv(params["raw_path"])
    df = clean(raw)
    print(f"Raw rows: {len(raw)}  ->  Clean rows: {len(df)}")

    train_df, test_df = train_test_split(
        df,
        test_size=params["test_size"],
        random_state=params["random_state"],
        stratify=df[TARGET],
    )
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    train_df.to_csv(f"{PROCESSED_DIR}/train.csv", index=False)
    test_df.to_csv(f"{PROCESSED_DIR}/test.csv", index=False)
    print(f"Train: {len(train_df)} rows, Test: {len(test_df)} rows")


if __name__ == "__main__":
    main()
