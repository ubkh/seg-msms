class GroupRestrictedMixin:
    """
    Mixin that only allows a specified group to access a view to users that are logged in.
    """

    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)
