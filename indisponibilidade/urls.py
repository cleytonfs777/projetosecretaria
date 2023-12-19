from django.urls import path

from . import views

urlpatterns = [
    # Indisponibilidade
    path('registrar_indisp/', views.registrar_indisp, name='registrar_indisp'),
    path('delete_indisp/<int:id_indisp>', views.delete_indisp, name='delete_indisp'),
    path('edit_indisp/<int:id_indisp>', views.edit_indisp, name='edit_indisp'),
    path('listar_indisp/', views.listar_indisp, name='listar_indisp'),
    # Feriados e Liberações
    path('registrar_ferlib/', views.registrar_ferlib, name='registrar_ferlib'),
    path('delete_ferlib/<int:id_ferlib>', views.delete_ferlib, name='delete_ferlib'),
    path('listar_ferlib/', views.listar_ferlib, name='listar_ferlib'),
    path('verificar_datas/', views.verificar_datas, name='verificar_datas'),
]

