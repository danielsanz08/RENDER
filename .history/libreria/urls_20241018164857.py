from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views
from libreria import views

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
    path('editar_perfil/<int:user_id>/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('ver_transacciones/', views.ver_transacciones, name='ver_transacciones'),
    path('crear_transacciones/', views.crear_transacciones, name='crear_transacciones'),
    path('registros_recientes/', views.registros_recientes, name='registros_recientes'),
    path('search/', views.search, name='search'),
    path('listar_usuario/', views.listar_usuario, name='listar_usuario'),
    path('transacciones/eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('agregar_insumo', views.agregar_insumo, name='agregar_insumo'),
    path('editar_insumo/<int:insumo_id>/', views.editar_insumo, name='editar_insumo'),
    path('verificar_nombre_insumo/', views.verificar_nombre_insumo, name='verificar_nombre_insumo'),
    path('verificar-administrador/', viewsverificar_administrador, name='verificar_administrador'),
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
        
    # URLs para productos
    path('productos/', views.productos, name='productos'),
    path('productos/lista_producto/', views.lista_productos, name='lista_productos'),  # Muestra la lista de productos
    path('productos/crear/', views.crear_producto, name='crear_producto'),  # Crear un nuevo producto
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),  # Eliminar un producto
    
    # URLs para clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('verificar_cliente/', views.verificar_cliente, name='verificar_cliente'),
    path('clientes/consultar_clientes', views.consultar_clientes, name='consultar_clientes'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    #URLS para proveedores
    path('crear/proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('listar_proveedor/', views.listar_proveedor, name='listar_proveedor'),
    path('editar/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('verificar_proveedor/', views.verificar_proveedor, name='verificar_proveedor'),
    path('reporte-excel.proveedor/', views.reporte_proveedor_excel, name='reporte_excel_proveedor'),
    path('reporte-pdf-proveedor/', views.reporte_proveedor_pdf, name='reporte_pdf_proveedor'),
    path('reporte-excel.insumo/', views.reporte_insumo_excel, name='reporte_excel_insumo'),
    path('reporte-pdf-insumo/', views.reporte_insumo_pdf, name='reporte_pdf_insumo'),
    path('reporte-excel.cliente/', views.reporte_cliente_excel, name='reporte_excel_cliente'),
    path('reporte-pdf-cliente/', views.reporte_cliente_pdf, name='reporte_pdf_cliente'),
    path('reporte-excel.producto/', views.reporte_producto_excel, name='reporte_excel_producto'),
    path('reporte-pdf-producto/', views.reporte_producto_pdf, name='reporte_pdf_producto'),
    path('reporte-excel.movimiento/', views.reporte_movimiento_excel, name='reporte_excel_movimiento'),
    path('reporte-pdf-movimiento/', views.reporte_movimiento_pdf, name='reporte_pdf_movimiento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)