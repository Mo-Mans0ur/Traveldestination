FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the full project (backend + templates + static)
COPY . /app

EXPOSE 5000

CMD ["python", "/app/backend/app.py"]