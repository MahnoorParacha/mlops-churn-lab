# Image that serves the churn API. Same image is used for Hugging Face and Azure.
FROM python:3.11-slim

WORKDIR /app

COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt

COPY api/ api/
COPY models/ models/

# Hugging Face expects port 7860. Azure will be told to use the same port.
ENV PORT=7860
EXPOSE 7860

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
