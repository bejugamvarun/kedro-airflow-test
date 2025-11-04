"""Airflow DAG for Kedro data processing pipeline."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator

from kedro_airflow_test.operators import KedroEcsRunTaskOperator

# Default DAG arguments
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'kedro_data_processing',
    default_args=default_args,
    description='Kedro data processing pipeline on ECS',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['kedro', 'data-processing', 'ecs'],
)

# Start task
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

# Kedro data processing task using custom ECS operator
# Option 1: Run entire pipeline (current approach)
# data_processing_task = KedroEcsRunTaskOperator(
#     task_id='run_data_processing_pipeline',
#     pipeline_name='data_processing',
#     package_name='kedro_airflow_test',
#     # ECS task configuration
#     task_id='kedro-data-processing-task',
#     task_definition='kedro-data-processing-task-def',
#     cluster='kedro-cluster',
#     subnets=['subnet-12345', 'subnet-67890'],  # Replace with actual subnet IDs
#     security_groups=['sg-12345'],  # Replace with actual security group ID
#     aws_conn_id='aws_default',
#     region_name='us-east-1',
#     # Environment variables for the pipeline
#     env={
#         'AWS_REGION': 'us-east-1',
#         'KEDRO_ENV': 'production',
#     },
#     dag=dag,
# )

# Option 2: Run individual nodes (recommended for better granularity)
# Uncomment the lines below to run individual nodes instead of entire pipeline
process_data_node_task = KedroEcsRunTaskOperator(
    task_id='run_process_data_node',
    pipeline_name='data_processing',
    node='process_data_node',  # Run only this specific node
    package_name='kedro_airflow_test',
    # ECS task configuration
    task_definition='kedro-data-processing-task-def',
    cluster='kedro-cluster',
    subnets=['subnet-12345', 'subnet-67890'],  # Replace with actual subnet IDs
    security_groups=['sg-12345'],  # Replace with actual security group ID
    aws_conn_id='aws_default',
    region_name='us-east-1',
    # Environment variables for the pipeline
    env={
        'AWS_REGION': 'us-east-1',
        'KEDRO_ENV': 'production',
    },
    dag=dag,
)

# End task
end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set task dependencies
start_task >> process_data_node_task >> end_task