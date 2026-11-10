"""Upload the release/ folder to a Hugging Face Docker Space.

Needs two environment variables:
  HF_TOKEN  - a Hugging Face access token with WRITE permission
  HF_SPACE  - your Space id, e.g.  your-username/churn-api
"""
import os

from huggingface_hub import HfApi

token = os.environ["HF_TOKEN"]
space = os.environ["HF_SPACE"]

api = HfApi(token=token)
api.upload_folder(
    folder_path="release",
    repo_id=space,
    repo_type="space",
    commit_message="Deploy from GitHub Actions",
)
user, name = space.split("/")
url = f"https://{user.lower()}-{name.lower().replace('_', '-')}.hf.space"
print(f"Uploaded. The Space will rebuild in 2-5 minutes.\nAPI URL: {url}/docs")
