# Dockerfile

# 1) Use a small, official Python image
FROM python:3.10-slim

# 2) Set working dir
WORKDIR /app

# 3) Install pip build tools & app deps
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel \
 && python3 -m pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of your app
COPY . .

# 5) Expose the port Cloud Run will use
EXPOSE 8080

# 6) Entrypoint: run your main Streamlit script, binding to $PORT and 0.0.0.0
ENTRYPOINT ["sh","-c","streamlit run 0_Background.py --server.port ${PORT:-8080} --server.address 0.0.0.0"]
