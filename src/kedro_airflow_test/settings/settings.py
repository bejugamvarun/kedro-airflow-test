"""Project settings."""

from kedro_airflow_test.hooks import ProjectHooks

# Configuration for different environments can be added here
# CONF_SOURCE = "conf"
# CONF_ROOT = "conf"

# Project hooks
HOOKS = (ProjectHooks(),)