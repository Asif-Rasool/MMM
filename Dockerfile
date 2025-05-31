# Use Python 3.11 as specified in runtime.txt
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including gcc for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .streamlit directories for secret mounting
RUN mkdir -p /app/.streamlit /workspace/.streamlit /home/cnb/.streamlit

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "0_Background.py", "--server.port=8501", "--server.address=0.0.0.0"]