from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    
     path('', views.login_view, name='login'),  # Añade esta línea
     path('logout_view/', views.logout_view, name='logout_view'),
    path('inicio/', views.inicio, name='inicio'),
    path('usuario/', views.usuario, name='usuario'),
    path('contabilidad/', views.contabilidad, name='contabilidad'),
    path('insumos/', views.insumos, name='insumos'),
    path('crear_perfil/', views.crear_perfil, name='crear_perfil'),
    
    path('login_view/', views.login_view, name='login_view'),
    path('ver_perfil/', views.ver_perfil, name='ver_perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('ver_transacciones/', views.ver_transacciones, name='ver_transacciones'),
    path('crear_transacciones/', views.crear_transacciones, name='crear_transacciones'),
    path('registros_recientes/', views.registros_recientes, name='registros_recientes'),
    path('search/', views.search, name='search'),
    path('listar_usuario/', views.listar_usuario, name='listar_usuario'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('agregar_insumo', views.agregar_insumo, name='agregar_insumo'),
     path('editar_insumo/<int:pk>/', views.editar_insumo, name='editar_insumo'),
    path('verificar_nombre_insumo/', views.verificar_nombre_insumo, name='verificar_nombre_insumo'),
    path('eliminar_insumo/<int:id>/', views.eliminar_insumo, name='eliminar_insumo'),
    path('consultar_insumo', views.consultar_insumo, name='consultar_insumo'),
    path('backup/', views.backup_view, name='backup'),
    path('backup/download/<int:id>/', views.download_backup, name='download_backup'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('activar_usuario/<int:id>/', views.activar_usuario, name='activar_usuario'),
    path('inactivar_usuario/<int:id>/', views.inactivar_usuario, name='inactivar_usuario'),
    path('toggle_user_status/<int:id>/', vietoggle_user_status, name='toggle_user_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)