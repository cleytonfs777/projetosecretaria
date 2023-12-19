
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('cadastros/', include('cadastros.urls')),
    path('indisponibilidade/', include('indisponibilidade.urls')),
]
