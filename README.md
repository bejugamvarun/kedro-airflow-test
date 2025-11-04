# Kedro Airflow Test

A Kedro project that demonstrates running data processing pipelines on AWS ECS via Apache Airflow (MWAA).

## Overview

This project contains a single-node Kedro pipeline that:
- Reads Parquet files from S3
- Performs Polars transformations (filtering, aggregation, feature engineering)
- Writes processed data back to S3

The pipeline is designed to run on AWS ECS through Apache Airflow MWAA using a custom ECS operator.

## Project Structure

```
├── conf/                    # Configuration files
│   ├── base/               # Base configuration
│   └── local/              # Local environment overrides
├── data/                   # Data directories (01_raw, 02_intermediate, etc.)
├── dags/                   # Airflow DAGs
├── docs/                   # Documentation
├── logs/                   # Log files
├── notebooks/              # Jupyter notebooks
├── src/kedro_airflow_test/ # Source code
│   ├── pipelines/          # Pipeline definitions
│   ├── operators.py        # Custom ECS operator
│   └── settings.py         # Project settings
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Local development
├── build-docker.sh         # Docker build script
└── pyproject.toml          # Project configuration
```

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure AWS credentials:**
   Set up your AWS credentials for S3 access and ECS permissions.

3. **Update configuration:**
   - Edit `conf/base/catalog.yml` with your S3 bucket paths
   - Update subnet IDs and security groups in `dags/kedro_data_processing_dag.py`

## Usage

### Local Development

1. **Run the pipeline locally:**
   ```bash
   kedro run
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up
   ```

### AWS Deployment

1. **Build and push Docker image:**
   ```bash
   ./build-docker.sh
   # Follow the ECR push instructions in the script
   ```

2. **Deploy to MWAA:**
   - Upload the DAG file to your MWAA environment
   - Ensure the ECS task definition and cluster are created
   - Update the DAG configuration with correct resource IDs

## Pipeline Details

The `data_processing` pipeline contains one node that performs:
- Data filtering (removes negative values)
- Feature engineering (doubles numeric columns, extracts year from dates)
- Aggregation (sums and averages by category)
- Sorting (by total doubled values)

## Configuration

### S3 Datasets
- **Input:** `s3://your-bucket/input/data.parquet`
- **Output:** `s3://your-bucket/output/processed_data.parquet`

### Environment Variables
- `KEDRO_ENV`: Environment (local/production)
- `AWS_REGION`: AWS region for S3 and ECS
- `KEDRO_PIPELINE`: Pipeline name to run

## MWAA Setup

1. Create an ECS cluster and task definition
2. Configure MWAA with appropriate permissions for ECS and S3
3. Upload the DAG and ensure the custom operator is available
4. Set up VPC networking for ECS task execution
