"""Project hooks."""

from kedro.framework.hooks import hook_impl


class ProjectHooks:
    """Project hooks for Kedro."""

    @hook_impl
    def register_config_loader(self, config_loader):
        """Register config loader."""
        pass

    @hook_impl
    def register_catalog(self, catalog):
        """Register catalog."""
        pass