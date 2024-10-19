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
    path('manual/', views.manual, name='manual'),
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
     path('cambiar-estado-usuario/<int:user_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
         # Rutas para la recuperación de contraseña usando vistas personalizadas
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='subject.txt',
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password_reset_complete/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)