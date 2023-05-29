FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the webhook receiver script into the container
COPY main.py .

# Set the entrypoint command to start the webhook receiver
ENTRYPOINT ["python", "main.py"]