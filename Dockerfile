# Use a lightweight Python base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all folders and files (src, data, models, etc.)
COPY . .

# Expose port 8501 for the Streamlit app (app.py)
EXPOSE 8501

# Default command to run the dashboard
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
