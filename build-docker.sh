#!/bin/bash
# Build script for Kedro Docker image

set -e

echo "Building Kedro Docker image..."

# Build the Docker image
docker build -t kedro-airflow-test:latest .

echo "Docker image built successfully!"

# Optional: Tag for ECR
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
# docker tag kedro-airflow-test:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/kedro-airflow-test:latest
# docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/kedro-airflow-test:latest

echo "To push to ECR, uncomment and update the commands above with your account ID."