# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG DEV=false
# Set the working directory in the container
WORKDIR /src

# Install dependencies
# COPY requirements.txt /app/
COPY requirements.txt /src/
COPY requirements.dev.txt /src/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && \
    if [ $DEV = "true" ]; \
            then  pip install --no-cache-dir -r requirements.dev.txt ; \
        fi 
#Copy the project files into the container
COPY . /src/
