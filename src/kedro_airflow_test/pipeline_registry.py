"""Project pipelines."""

from typing import Dict

from kedro.pipeline import Pipeline

from kedro_airflow_test.pipelines.data_processing import create_pipeline as create_data_processing_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_processing_pipeline = create_data_processing_pipeline()

    return {
        "__default__": data_processing_pipeline,
        "data_processing": data_processing_pipeline,
    }