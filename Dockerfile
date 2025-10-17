# Step 1: Base Image
FROM python:3.8-slim

# Step 2: Install vulnerable package version (example)
RUN apt-get update && apt-get install -y --no-install-recommends openssl

# Step 3: Copy app files
COPY app /app

# Step 4: Set working directory
WORKDIR /app

# Step 5: Command to run app
CMD ["python3", "app.py"]
