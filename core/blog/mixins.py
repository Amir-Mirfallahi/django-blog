from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user is the object's owner."""
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user.profile:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
