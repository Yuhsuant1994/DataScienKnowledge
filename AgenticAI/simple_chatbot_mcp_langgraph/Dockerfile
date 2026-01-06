# Use an official Python 3.11 runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install backend requirements (includes all dependencies including MCP)
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip3 install --default-timeout=100 -v -r /app/requirements.txt

# Copy backend app (includes mcp_server inside app/)
COPY backend/app /app/app
COPY backend/.env /app/.env

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
