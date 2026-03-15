FROM python:3.11-slim

# Set the workdir to /app (Internal container path)
WORKDIR /app

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard] pydantic joblib pandas scikit-learn

# 2. Copy the folders into the container
# This preserves the /src and /models structure
COPY src/ ./src/
COPY models/ ./models/

EXPOSE 8000

# 3. Start the app
# Points to src/api.py (FastAPI 'app' object)
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
