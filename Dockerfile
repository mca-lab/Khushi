# Python base image
FROM python:3.10-slim

# Install Java (required for PySpark)
RUN apt-get update && apt-get install -y default-jdk && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME manually
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Create app folder
WORKDIR /app

# Copy everything to container
COPY . /app

# Install PySpark + Requests
RUN pip install --no-cache-dir pyspark requests

# Run your cleaning script
CMD ["python", "src/clean_data.py"]
