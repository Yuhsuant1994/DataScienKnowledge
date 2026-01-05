# Use an official Python 3.9 runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install first part of packages
COPY requirements.txt /app
# RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip3 install --default-timeout=100  -v -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /app
COPY ./.env /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
