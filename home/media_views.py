import posixpath

from django.http import Http404
from django.views.static import serve

from .models import OvozJavob


def public_media(request, path, **kwargs):
    normalized = posixpath.normpath(path.replace('\\', '/')).lstrip('/')
    if normalized.casefold().startswith('ovoz/') or OvozJavob.objects.filter(fayl=normalized).exists():
        raise Http404
    return serve(request, path, **kwargs)
