from rolepermissions.roles import AbstractUserRole


class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_gerentes': True,
        'cadastrar_usuario': True,
    }

class Usuario(AbstractUserRole):
    available_permissions = {
        'cadastrar_usuario': False,
    }