from rest_framework.permissions import BasePermission, SAFE_METHODS

class PermissaoOrganizacao(BasePermission):
    def has_permission(self, request, view):
        perfil = getattr(request.user, 'perfil', None)
        if not request.user.is_authenticated or perfil is None:
            return False
        return request.method in SAFE_METHODS or perfil.eh_admin or (getattr(view, 'operador_cria', False) and request.method == 'POST')
