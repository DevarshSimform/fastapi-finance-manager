FROM python:3.11-slim

WORKDIR /app

# Copy requirements if you have one, else pip install here
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

EXPOSE 8000

# Default command to start FastAPI app; can override in docker-compose for notification
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
