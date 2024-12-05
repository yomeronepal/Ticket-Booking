# Use an official Python runtime as a parent image
FROM python:3.9.16-alpine

# Set the working directory in the container
WORKDIR /app
# Install build dependencies and libraries needed for PostgreSQL, Kafka, and others
RUN apk --no-cache add \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    postgresql-dev \
    librdkafka-dev \
    bash \
    make \
    curl
# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development  
# RUN flask db upgrade
# Run the application
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
CMD flask db upgrade && flask run --host=0.0.0.0 --port=8000
