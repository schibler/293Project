# Use official Python 3.7 slim image as base
FROM python:3.7-slim

# Set working directory inside the container
WORKDIR /pensieve

# Install system dependencies (for any builds/tools you may need)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip setuptools wheel

# Install TensorFlow 1.15 (CPU version)
RUN pip install tensorflow==1.15

# Install tflearn compatible with TF1.15
RUN pip install tflearn==0.3.2

RUN pip install protobuf==3.20.3
RUN pip install matplotlib

# Copy your Pensieve code into the container (optional, you can also mount)
# COPY . /pensieve

# Set environment variable so TF 1.x behavior is default
ENV TF_ENABLE_CONTROL_FLOW_V2=0

# Default command (optional, override with your own)
CMD ["/bin/bash"]
