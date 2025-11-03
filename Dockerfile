# ===== Base image with OpenJDK 17 =====
FROM openjdk:17-jdk-slim

# ===== Set environment variables for Java =====
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# ===== Install system dependencies =====
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-dev build-essential \
        curl wget git procps unzip && \
    rm -rf /var/lib/apt/lists/*

# ===== Set Python environment for PySpark =====
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# ===== Spark & Hadoop versions =====
ENV SPARK_VERSION=3.5.2
ENV HADOOP_VERSION=3

# ===== Download and install Spark =====
RUN curl -L "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    -o /tmp/spark.tgz && \
    tar -xzf /tmp/spark.tgz -C /opt/ && \
    rm /tmp/spark.tgz

# ===== Set Spark environment variables =====
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH="$SPARK_HOME/bin:$PATH"

# ===== Hadoop environment (standalone mode) =====
ENV HADOOP_HOME=$SPARK_HOME
ENV HADOOP_CONF_DIR=$SPARK_HOME/conf
ENV PATH=$HADOOP_HOME/bin:$PATH

# ===== Install Python packages =====
RUN pip3 install --no-cache-dir pyspark pandas kaggle

# ===== Set working directory =====
WORKDIR /app

# ===== Copy project files =====
COPY . .

# ===== Expose Spark UI port =====
EXPOSE 4040

# ===== Default command to run your scripts =====
CMD ["bash", "-c", "set -e; python3 fetch_data.py && python3 clean_data.py"]