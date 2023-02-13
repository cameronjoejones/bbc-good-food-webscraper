# Use an official Python runtime as the base image
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install pipenv and the dependencies
RUN apk add --no-cache --update build-base \
    && pip install pipenv \
    && pipenv install --system --ignore-pipfile

# Copy the rest of the code to the container
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
