# myapp/middleware.py

from django.utils.deprecation import MiddlewareMixin

class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtener la lista de breadcrumbs de la sesión
        breadcrumbs = request.session.get('breadcrumbs', [])
        
        # Obtener la URL actual
        current_path = request.path
        
        # Agregar la URL actual a los breadcrumbs si no es la página de inicio
        if current_path != '/':
            if not breadcrumbs or breadcrumbs[-1]['url'] != current_path:
                breadcrumbs.append({'title': self.get_page_title(request), 'url': current_path})
        
        # Guardar los breadcrumbs en la sesión
        request.session['breadcrumbs'] = breadcrumbs

    def process_response(self, request, response):
        # Limpiar los breadcrumbs si el usuario sale de la página actual
        if request.path == '/':
            request.session['breadcrumbs'] = [{'title': 'Inicio', 'url': '/'}]
        return response

    def get_page_title(self, request):
        # Aquí puedes implementar una lógica para obtener el título de la página basado en la URL
        # Por simplicidad, se devuelve una cadena fija, pero deberías adaptar esto según tu necesidad
        url_mapping = {
            '/': 'Inicio',
            '/contabilidad/': 'Contabilidad',
            '/usuario': 'Usuario',
            '/crear_perfil'
            
            # Agrega más mapeos de URL a títulos aquí
        }
        return url_mapping.get(request.path, 'Página Desconocida')
