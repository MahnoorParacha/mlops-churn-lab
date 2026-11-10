# Image that serves the churn API. Same image is used for Hugging Face and Azure.
FROM python:3.11-slim

WORKDIR /app

# TODO S2.6: Copy requirements-serving.txt and install it with pip.
# Hint: COPY <file> .   then   RUN pip install --no-cache-dir -r <file>
# COPY ... and RUN pip install ...

# TODO S2.7: Copy the api/ folder and the models/ folder into the image.
# COPY api/ ... and COPY models/ ...

# Hugging Face expects port 7860. Azure will be told to use the same port.
ENV PORT=7860
EXPOSE 7860

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
