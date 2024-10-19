from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='home'),
    path('', views.index, name='index'),
    path('inicio', views.inicio, name='inicio'),
    path('usuario', views.usuario, name='usuario'),
    path('contabilidad', views.contabilidad, name='contabilidad'),
    path('insumos', views.insumos, name='insumos'),
    path('ver_perfil', views.ver_perfil, name='ver_perfil'),
    path('editar_perfil', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contraseña', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('ver_transacciones', views.ver_transacciones, name='ver_transacciones'),
    path('crear_transacciones', views.crear_transacciones, name='crear_transacciones'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)