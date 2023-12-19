from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar_militar/', views.cadastrar_militar, name='cadastrar_militar'),
    path('delete_militar/<int:id_militar>', views.delete_militar, name='delete_militar'),
    path('edit_militar/<int:id_militar>', views.edit_militar, name='edit_militar'),
    path('cadastrar_empenho/', views.cadastrar_empenho, name='cadastrar_empenho'),
    path('editar_empenho/<int:id_empenho>', views.editar_empenho, name='editar_empenho'),
    path('delete_empenho/<int:id_empenho>', views.delete_empenho, name='delete_empenho'),
    path('edit_empenho/<int:id_empenho>', views.edit_empenho, name='edit_empenho'),
    path('registrar_empenho/', views.registrar_empenho, name='registrar_empenho'),
    path('listar_cadastros/', views.listar_cadastros, name='listar_cadastros'),
    path('get_empenhos/<int:militar_id>/', views.get_empenhos, name='get_empenhos'),
    path('get_mil_data/<int:militar_id>/', views.get_mil_data, name='get_mil_data'),
    path('is_permited_empenho/<int:militar_id>/<int:empenho_id>/', views.is_permited_empenho, name='is_permited_empenho')

]