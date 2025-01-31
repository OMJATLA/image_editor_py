FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies directly
RUN pip install --no-cache-dir fastapi uvicorn requests python-multipart

# Copy the application code
COPY . .

# Expose the FastAPI default port
EXPOSE 8090

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8090", "--reload"]
