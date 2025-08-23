# Use a small official Python image as the base
FROM python:3.12-slim

# Ensure output is flushed (helpful for logs in containers)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create and switch to the app directory inside the image
WORKDIR /app

# Install dependencies separately for better Docker layer caching
# 1) Copy only requirements first, then install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 2) Copy the rest of the project files
COPY . /app

# Expose the port Uvicorn will listen on
EXPOSE 8000

# Start the API with Uvicorn (bind to 0.0.0.0 so Docker can map the port)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
