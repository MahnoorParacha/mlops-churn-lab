"""Stage 1: download the raw dataset (Telco Customer Churn)."""
import os
import urllib.request

from src.config import load_params


def main():
    params = load_params()["data"]
    os.makedirs(os.path.dirname(params["raw_path"]), exist_ok=True)
    print(f"Downloading {params['url']}")
    urllib.request.urlretrieve(params["url"], params["raw_path"])
    print(f"Saved to {params['raw_path']}")


if __name__ == "__main__":
    main()
