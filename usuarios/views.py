from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator

from .models import Usuario


def authenticate_username_or_email(username, password):
    try:
        user = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        try:
            user = Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            return None

    if user.check_password(password):
        return user


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'login.html')
    elif request.method == "POST":
        username_or_email = request.POST.get('username')
        senha = request.POST.get('password')

    user = authenticate_username_or_email(username_or_email, senha)

    if not user:
        messages.add_message(request, messages.ERROR,
                             "O usuário e/ou a senha estão incorretos")
        return redirect(reverse('login'))

    auth.login(request, user)
    return redirect(reverse('home'))


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


@login_required
def home(request):
    return render(request, 'home.html')
