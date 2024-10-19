from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='home'),
    
    path('inicio/', views.inicio, name='inicio'),
    path('usuario/', views.usuario, name='usuario'),
    path('contabilidad/', views.contabilidad, name='contabilidad'),
    path('insumos/', views.insumos, name='insumos'),
    path('ver_perfil/', views.ver_perfil, name='ver_perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('ver_transacciones/', views.ver_transacciones, name='ver_transacciones'),
    path('crear_transacciones/', views.crear_transacciones, name='crear_transacciones'),
    path('search/', views.search, name='search'),
    path('listar_usuario/', views.listar_usuario, name='buscar_usuario'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('agregar_insumo', views.agregar_insumo, name='agregar_insumo'),
    path('editar_insumo', views.editar_insumo, name='editar_insumo'),
    path('eliminar_insumo/<int:id>/', views.eliminar_insumo, name='eliminar_insumo'),
    path('consultar_insumo', views.consultar_insumo, name='consultar_insumo')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)