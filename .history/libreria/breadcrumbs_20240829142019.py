# breadcrumbs.py

from django.urls import reverse
from functools import wraps

class Breadcrumb:
    def __init__(self, name, url_name, args=None, kwargs=None):
        self.name = name
        self.url_name = url_name
        self.args = args or []
        self.kwargs = kwargs or {}

    @property
    def url(self):
        return reverse(self.url_name, args=self.args, kwargs=self.kwargs)

class Breadcrumbs:
    def __init__(self):
        self.trail = []

    def add(self, name, url_name, args=None, kwargs=None):
        self.trail.append(Breadcrumb(name, url_name, args, kwargs))

    def __iter__(self):
        return iter(self.trail)

def breadcrumb(name, url_name, args=None, kwargs=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *view_args, **view_kwargs):
            if not hasattr(request, 'breadcrumbs'):
                request.breadcrumbs = Breadcrumbs()
            request.breadcrumbs.add(name, url_name, args, kwargs)
            return view_func(request, *view_args, **view_kwargs)
        return wrapped_view
    return decorator