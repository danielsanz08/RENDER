from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import timedelta
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.db import transaction, connections
from django.core import management
from django.contrib.auth import get_user_model
from django import db
from pandas import Timedelta
from .models import Backup
from .utils import crear_backup, restaurar_backup
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

def error_404_view(request, exception):
    return render(request, 'acceso_denegado.html', status=404)

def timeouterror(request):
    try:
        raise TimeoutError("Error de tiempo de espera")
        return render(request, 'exito.html')
    except TimeoutError:
        return render(request, 'lan_error.html')

@login_required(login_url='/acceso_denegado/')
def index_backup(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': 'index_backup'}
    ]
    return render(request, 'backup/index.html', {'breadcrumbs': breadcrumbs})

@login_required(login_url='/acceso_denegado/')
def lista_backups(request):
    breadcrumbs = [
        
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Lista de backups', 'url': reverse('backup:lista_backups')},
    ]
    
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    
    backups = Backup.objects.all().order_by('-fecha_creacion')

    if query:
        backups = backups.annotate(
            fecha_creacion_str=Cast('fecha_creacion', CharField()),
            creado_por_str=Cast('creado_por__username', CharField())
        ).filter(
            Q(nombre__icontains=query) |
            Q(fecha_creacion_str__icontains=query) |
            Q(creado_por_str__icontains=query)
        )

    try:
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            backups = backups.filter(fecha_creacion__gte=fecha_inicio)

        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() + timedelta(days=1)
            backups = backups.filter(fecha_creacion__lt=fecha_fin)
    except ValueError:
        backups = Backup.objects.none()

    paginator = Paginator(backups, 4)
    page_number = request.GET.get('page')
    backups_page = paginator.get_page(page_number)

    query_params = ''
    if query:
        query_params += f'&q={query}'
    if fecha_inicio_str:
        query_params += f'&fecha_inicio={fecha_inicio_str}'
    if fecha_fin_str:
        query_params += f'&fecha_fin={fecha_fin_str}'

    return render(request, 'backup/listar.html', {
        'backups': backups_page,
        'breadcrumbs': breadcrumbs,
        'query_params': query_params,
        'current_query': query,
        'current_fecha_inicio': fecha_inicio_str,
        'current_fecha_fin': fecha_fin_str,
    })
@login_required(login_url='/acceso_denegado/')
def crear_nuevo_backup(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Crear backups', 'url': reverse('backup:crear_backup')},
    ]

    if request.method == 'POST':
        try:
            nombre_archivo, ruta_archivo = exportar_bd()
            
            tamano = os.path.getsize(ruta_archivo)
            tamano_mb = round(tamano / (1024 * 1024), 2)
            nombre = request.POST.get('nombre') or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo, cafeteria.Productos, cafeteria.Pedido, cafeteria.PedidoProducto, cde.PedidoCde, cde.PedidoProductoCde (con relaciones)",
                creado_por=request.user
            )

            with open(ruta_archivo, 'rb') as f:
                backup.archivo.save(nombre_archivo, f)

            messages.success(request, 'Copia de seguridad creada exitosamente con todas las relaciones.')
            return redirect('backup:lista_backups')

        except Exception as e:
            print("❌ ERROR EN CREAR BACKUP:", e)
            logger.error(f"Error al crear backup: {str(e)}", exc_info=True)
            messages.error(request, f'Error al crear copia de seguridad: {str(e)}')
            return redirect('backup:crear_backup')

    return render(request, 'backup/crear.html', {'breadcrumbs': breadcrumbs})

@login_required(login_url='/acceso_denegado/')
def restaurar_backup_view(request, id):
    user_id = request.user.id
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Restaurar backup', 'url': reverse('backup:restaurar_backup', kwargs={'id': id})},
    ]

    backup = get_object_or_404(Backup, id=id)
    
    try:
        ruta_absoluta = os.path.join(settings.MEDIA_ROOT, backup.archivo.name)

        if not os.path.exists(ruta_absoluta):
            messages.error(request, f"El archivo de backup no existe en {ruta_absoluta}")
            return redirect('backup:lista_backups')

        
        from django.contrib.auth import logout
        logout(request)
        request.session.flush()
        
        db.connections.close_all()

        try:
            import json
            with open(ruta_absoluta, 'r', encoding='utf-8') as f:
                json.load(f)
        except Exception as json_error:
            logger.error(f"Archivo de backup inválido: {str(json_error)}", exc_info=True)
            messages.error(request, "El archivo de backup es inválido o está corrupto. La base de datos no ha sido alterada.")
            return redirect('backup:lista_backups')

        try:
            connection = connections['default']
            
            with connection.cursor() as cursor:
                cursor.execute("SET SESSION wait_timeout = %s", [28800])
                cursor.execute("SET SESSION interactive_timeout = %s", [28800])
                cursor.execute("SET FOREIGN_KEY_CHECKS = %s", [0])
                
                management.call_command('flush', interactive=False, verbosity=0)
                
                restaurar_backup(ruta_absoluta)
                
                try:
                    cursor.execute("SET FOREIGN_KEY_CHECKS = %s", [1])
                    cursor.execute("ANALYZE TABLE")
                except Exception as analyze_error:
                    logger.warning(f"Error al ejecutar ANALYZE TABLE: {str(analyze_error)}")
                
                connection.commit()

        except db.Error as e:
            logger.error(f"Error de base de datos durante restauración: {str(e)}", exc_info=True)
            messages.error(request, f'Error de base de datos al restaurar: {str(e)}')
            return redirect('libreria:inicio')
        except Exception as e:
            logger.error(f"Error inesperado durante restauración: {str(e)}", exc_info=True)
            messages.error(request, f'Error técnico al restaurar: {str(e)}')
            return redirect('libreria:inicio')

        messages.success(request, 'Copia de seguridad restaurada exitosamente. Por favor inicie sesión nuevamente.')
        return redirect('libreria:inicio')

    except Exception as e:
        logger.error(f"Error general al restaurar backup: {str(e)}", exc_info=True)
        messages.error(request, f'Error al restaurar copia de seguridad: {str(e)}')
        return redirect('libreria:inicio')
    

@login_required(login_url='/acceso_denegado/')
def descargar_backup(request, id):
    try:
        backup = get_object_or_404(Backup, id=id)
        response = FileResponse(open(backup.archivo.path, 'rb'), as_attachment=True)
        response['Content-Length'] = os.path.getsize(backup.archivo.path)
        return response
    except Exception as e:
        logger.error(f"Error al descargar backup: {str(e)}", exc_info=True)
        messages.error(request, f'Error al descargar archivo: {str(e)}')
        return redirect('backup:lista_backups')

@login_required(login_url='/acceso_denegado/')
def eliminar_backup(request, id):
    try:
        backup = get_object_or_404(Backup, id=id)
        if os.path.exists(backup.archivo.path):
            os.remove(backup.archivo.path)
        backup.delete()
        messages.success(request, 'Copia de seguridad eliminada exitosamente.')
    except Exception as e:
        logger.error(f"Error al eliminar backup: {str(e)}", exc_info=True)
        messages.error(request, f'Error al eliminar copia de seguridad: {str(e)}')
    return redirect('backup:lista_backups')

def exportar_bd(nombre_archivo=None):
    """Función mejorada para exportar la base de datos completa con relaciones"""
    if not nombre_archivo:
        nombre_archivo = f"backup_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    ruta_backup = os.path.join(settings.BACKUP_ROOT, nombre_archivo)

    try:
        with open(ruta_backup, 'w', encoding='utf-8') as f:
            management.call_command(
                'dumpdata',
                stdout=f,
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
                indent=4,
                exclude=['contenttypes', 'auth.permission', 'sessions.session']
            )
        return nombre_archivo, ruta_backup
    except Exception as e:
        logger.error(f"Error al exportar BD: {str(e)}", exc_info=True)
        raise Exception(f"Error al exportar la base de datos: {str(e)}")

@login_required(login_url='/acceso_denegado/')
def exportar(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Exportar BD', 'url': reverse('backup:exportar_backup')},
    ]

    try:
        nombre_archivo, ruta_backup = exportar_bd()

        if not os.path.exists(ruta_backup):
            messages.error(request, 'El archivo de respaldo no se encontró.')
            return redirect('backup:lista_backups')

        tamano = os.path.getsize(ruta_backup)
        tamano_mb = round(tamano / (1024 * 1024), 2)

        backup = Backup(
            nombre=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            tamano=f"{tamano_mb} MB",
            modelos_incluidos="Todos (exportación completa con relaciones)",
            creado_por=request.user
        )

        with open(ruta_backup, 'rb') as f:
            backup.archivo.save(nombre_archivo, f, save=False)

        backup.save()

        response = FileResponse(open(ruta_backup, 'rb'), as_attachment=True, filename=nombre_archivo)
        messages.success(request, 'Base de datos exportada exitosamente con todas las relaciones.')
        return response

    except Exception as e:
        logger.error(f"Error en exportar(): {str(e)}", exc_info=True)
        messages.error(request, f'Error al exportar la base de datos: {str(e)}')
        return redirect('backup:lista_backups')

@login_required(login_url='/acceso_denegado/')
def importar_backup_view(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Importar backup', 'url': reverse('backup:importar')},
    ]

    if request.method == 'POST':
        try:
            archivo_subido = request.FILES['archivo']
            nombre = request.POST.get('nombre', f"backup_importado_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            carpeta_backups = os.path.join(settings.MEDIA_ROOT, 'backups')
            os.makedirs(carpeta_backups, exist_ok=True)
            nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{archivo_subido.name}"
            ruta_completa = os.path.join(carpeta_backups, nombre_archivo)

            with open(ruta_completa, 'wb+') as destino:
                for chunk in archivo_subido.chunks():
                    destino.write(chunk)

            tamano = os.path.getsize(ruta_completa)
            tamano_mb = round(tamano / (1024 * 1024), 2)
            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="Todos (backup completo con relaciones)",
                creado_por=request.user
            )
            with open(ruta_completa, 'rb') as f:
                backup.archivo.save(nombre_archivo, f, save=False)
            backup.save()

            if 'restaurar' in request.POST:
                return redirect('backup:restaurar_backup', id=backup.id)

            messages.success(request, 'Backup importado exitosamente.')
            return redirect('backup:lista_backups')

        except Exception as e:
            logger.error(f"Error en importar_backup_view: {str(e)}", exc_info=True)
            messages.error(request, f'Error al importar el backup: {str(e)}')
            return redirect('backup:importar')

    return render(request, 'backup/importar.html', {'breadcrumbs': breadcrumbs})