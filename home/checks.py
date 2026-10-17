from pathlib import Path

from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.security)
def private_books_location(app_configs, **kwargs):
    return _private_location(settings.PRIVATE_BOOKS_ROOT, 'PRIVATE_BOOKS_ROOT', 'home.E001')


@register(Tags.security)
def private_voices_location(app_configs, **kwargs):
    return _private_location(settings.PRIVATE_VOICES_ROOT, 'PRIVATE_VOICES_ROOT', 'home.E002')


def _private_location(location, label, error_id):
    root = Path(location).resolve()
    public_roots = [settings.MEDIA_ROOT, *settings.STATICFILES_DIRS]
    if settings.STATIC_ROOT:
        public_roots.append(settings.STATIC_ROOT)
    errors = []
    for public in public_roots:
        if isinstance(public, (tuple, list)):
            public = public[1]
        if public:
            public = Path(public).resolve()
            if root.is_relative_to(public) or public.is_relative_to(root):
                errors.append(Error(
                    f'{label} media/static papkalaridan alohida bo‘lishi kerak.',
                    id=error_id,
                ))
                break
    return errors
