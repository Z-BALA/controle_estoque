from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Perfil

def org_atual(request):
    try:
        return request.user.perfil.organizacao
    except Perfil.DoesNotExist:
        raise PermissionDenied('Usuário sem organização. Solicite um perfil ao administrador do sistema.')

def acesso(admin=False):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            org_atual(request)
            if admin and not request.user.perfil.eh_admin:
                raise PermissionDenied('Acesso reservado ao administrador.')
            return view(request, *args, **kwargs)
        return wrapped
    return decorator
