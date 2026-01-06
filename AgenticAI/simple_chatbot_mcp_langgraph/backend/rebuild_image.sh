#!/bin/bash

# chmod +x rebuild_image.sh ; ./rebuild_image.sh

# Stop and remove the current running container (if it exists)
docker stop simple_chatbot
docker rm simple_chatbot



# Remove the existing image (if it exists)
# This step is optional and could be skipped to take advantage of Docker's caching mechanism
docker rmi simple_chatbot_image
# docker volume rm entreprise-search-volume

# Build the Docker image
docker build --no-cache -t simple_chatbot_image .

# Run the Docker container with a bind mount from the current ./backend directory
docker run -d \
  --network=bridge \
  --name simple_chatbot \
  -p 8001:80 \
  --env-file .env \
  -v .:/app \
  simple_chatbot_image \
  uvicorn app.main:app --reload --host 0.0.0.0 --port 80
