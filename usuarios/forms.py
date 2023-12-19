from django import forms
from django.contrib.auth import forms as auth_forms

from .models import Usuario


class UsuarioChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = Usuario


class UsuarioCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = Usuario