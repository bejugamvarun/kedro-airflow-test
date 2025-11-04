"""Main entry point for the Kedro project."""

from pathlib import Path

from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project


def main():
    """Run the Kedro project."""
    # Bootstrap the project
    bootstrap_project(Path(__file__).parent)

    # Configure the project
    configure_project("kedro_airflow_test.settings")

    # Create and run a session
    with KedroSession.create() as session:
        session.run()


if __name__ == "__main__":
    main()
