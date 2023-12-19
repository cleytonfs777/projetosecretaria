from django.contrib import admin
from django.contrib.auth import admin as admin_auth_django

from .forms import UsuarioChangeForm, UsuarioCreationForm
from .models import Usuario


@admin.register(Usuario)
class UserAdmin(admin_auth_django.UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    list_display = ['username', 'email', 'cargo']
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        (None, {'fields': ('cargo',)}),
    )
    add_fieldsets = admin_auth_django.UserAdmin.add_fieldsets + (
        (None, {'fields': ('cargo',)}),
    )


admin.register(Usuario)
