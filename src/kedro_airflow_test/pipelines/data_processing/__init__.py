"""Data processing pipeline."""

from kedro.pipeline import Pipeline, node

from .nodes import process_data


def create_pipeline(**kwargs) -> Pipeline:
    """Create the data processing pipeline."""
    return Pipeline(
        [
            node(
                func=process_data,
                inputs="input_data",
                outputs="processed_data",
                name="process_data_node",
            ),
        ]
    )