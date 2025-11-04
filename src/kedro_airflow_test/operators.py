"""Custom ECS operator for Kedro pipelines."""

from typing import Any, Dict, Optional

from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from kedro_airflow.operators.kedro import KedroOperator


class KedroEcsRunTaskOperator(EcsRunTaskOperator):
    """Custom ECS operator that extends EcsRunTaskOperator for Kedro pipelines.

    This operator runs Kedro pipelines or individual nodes on AWS ECS tasks within MWAA.
    When a node is specified, only that specific node will be executed.
    """

    def __init__(
        self,
        task_id: str,
        pipeline_name: str,
        package_name: str = "kedro_airflow_test",
        node: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Kedro ECS operator.

        Args:
            task_id: Airflow task ID
            pipeline_name: Name of the Kedro pipeline to run
            package_name: Name of the Kedro package
            node: Specific node name to run (if None, runs entire pipeline)
            env: Environment variables to pass to the ECS task
            **kwargs: Additional arguments for EcsRunTaskOperator
        """
        # Set default ECS task configuration
        default_overrides = {
            "containerOverrides": [
                {
                    "name": "kedro-container",
                    "environment": [
                        {"name": "KEDRO_PIPELINE", "value": pipeline_name},
                        {"name": "KEDRO_PACKAGE", "value": package_name},
                    ],
                }
            ]
        }

        # Add node parameter if specified
        if node:
            default_overrides["containerOverrides"][0]["environment"].append(
                {"name": "KEDRO_NODE", "value": node}
            )

        # Merge with provided overrides
        if "overrides" in kwargs:
            if "containerOverrides" in kwargs["overrides"]:
                # Merge container overrides
                existing_overrides = kwargs["overrides"]["containerOverrides"]
                default_overrides["containerOverrides"][0]["environment"].extend(
                    existing_overrides[0].get("environment", [])
                )
            kwargs["overrides"].update(default_overrides)
        else:
            kwargs["overrides"] = default_overrides

        # Add environment variables if provided
        if env:
            env_vars = [
                {"name": key, "value": value}
                for key, value in env.items()
            ]
            kwargs["overrides"]["containerOverrides"][0]["environment"].extend(env_vars)

        super().__init__(task_id=task_id, **kwargs)

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the ECS task with Kedro pipeline."""
        # Add any additional Kedro-specific logic here if needed
        return super().execute(context)