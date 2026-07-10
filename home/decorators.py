from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """View'ga faqat ko'rsatilgan roldagi foydalanuvchilarni kiritadi.

    Misol:
        @role_required('superadmin')
        @role_required('superadmin', 'tarbiyachi')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


superadmin_required = role_required('superadmin')
tarbiyachi_required = role_required('tarbiyachi')
oquvchi_required = role_required('oquvchi')
