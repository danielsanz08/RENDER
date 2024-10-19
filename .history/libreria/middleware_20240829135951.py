from django.utils.deprecation import MiddlewareMixin

class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        breadcrumbs = request.session.get('breadcrumbs', [])
        current_path = request.path
        url_mapping = {
            '/': 'Inicio',
            '/inicio/': 'Inicio',
            '/usuario/': 'Usuario',
            '/contabilidad/': 'Contabilidad',
            '/insumos/': 'Insumos',
            '/crear_perfil/': 'Crear Perfil',
            '/ver_perfil/': 'Ver Perfil',
            '/editar_perfil/': 'Editar Perfil',
            '/cambiar_contraseña/': 'Cambiar Contraseña',
            '/ver_transacciones/': 'Ver Transacciones',
            '/crear_transacciones/': 'Crear Transacciones',
            '/registros_recientes/': 'Registros Recientes',
            '/search/': 'Buscar',
            '/listar_usuario/': 'Listar Usuario',
            '/backup/': 'Backup',
            '/backup/download/': 'Descargar Backup',
        }
        current_title = url_mapping.get(current_path, 'Página Desconocida')
        if current_path != '/':
            if not breadcrumbs or breadcrumbs[-1]['url'] != current_path:
                breadcrumbs.append({'title': current_title, 'url': current_path})
        request.session['breadcrumbs'] = breadcrumbs

    def process_response(self, request, response):
        if request.path == '/':
            request.session['breadcrumbs'] = [{'title': 'Inicio', 'url': '/'}]
        return response
