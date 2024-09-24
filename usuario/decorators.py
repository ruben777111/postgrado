from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def usuario_administrador_required(view_func=None, login_url=None):
    actual_decorator = staff_member_required(login_url=login_url)

    def _decorator(view_func):
        @wraps(view_func)
        
        def _wrapped_view(request, *args, **kwargs):
            
            if not request.user.usuario_administrador:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if view_func:
        return _decorator(view_func)
    return _decorator
