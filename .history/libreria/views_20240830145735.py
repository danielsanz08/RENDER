from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Transaccion, Insumo, CustomUser, Backup
from django.contrib.auth.decorators import login_required
from .forms import InsumoForm, TransaccionForm, CustomUserCreationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from .utils import create_backup, restore_backup
import os
from .forms import CustomPasswordChangeForm
@login_required
def inicio(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': None},
    ]
    return render(request, 'index/index.html', {'breadcrumbs': breadcrumbs})

@login_required
def usuario(request):
    usuario = request.user  # Obtiene el usuario actual que ha iniciado sesión
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuario', 'url': None},
    ]
    return render(request, 'usuario/usuario.html', {'usuario': usuario,'breadcrumbs': breadcrumbs})

@login_required
def contabilidad(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Contabilidad', 'url': None},
    ]
    return render(request, 'transacciones/transacciones.html', {'breadcrumbs': breadcrumbs})

@login_required
def insumos(request):
    return render(request, 'insumos/insumos.html')

@login_required
def ver_perfil(request):
    usuario = request.user  # Obtiene el usuario actual que ha iniciado sesión
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Ver Perfil', 'url': None},
    ]
    return render(request, 'usuario/ver.html', {'usuario': usuario, 'breadcrumbs': breadcrumbs})


@login_required
def editar_perfil(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Editar Perfil', 'url': None},
    ]
    return render(request, 'usuario/editar.html', {'breadcrumbs': breadcrumbs})

@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito. Puedes iniciar sesión con tu nueva contraseña.')
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            messages.error(request, 'Hubo un error al cambiar tu contraseña. Por favor, inténtalo de nuevo.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'usuario/usuario.html', {'form': form})
@login_required
def listar_usuario(request):
    usuarios = CustomUser.objects.all()
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuarios', 'url': None},
        {'name': 'Listar Usuarios', 'url': None},
    ]
    return render(request, 'usuario/listar.html', {'usuarios': usuarios, 'breadcrumbs': breadcrumbs})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            user = authenticate(request, name=name, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('inicio')  # Redirige a la página principal o a otra página
            else:
                messages.error(request, 'Nombre o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  # Redirige a la página de inicio de sesión u otra página deseada

@login_required
def crear_perfil(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.email} creado exitosamente.')
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomUserCreationForm()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Crear Perfil', 'url': None},
    ]

    return render(request, 'usuario/registro.html', {'form': form, 'breadcrumbs': breadcrumbs})

@login_required
def crear_transacciones(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            nueva_transaccion = form.save(commit=False)
            nueva_transaccion.save()
            messages.success(request, 'Transacción creada exitosamente.')
            return redirect('registros_recientes')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = TransaccionForm()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Transacciones', 'url': '/ver_transacciones/'},
        {'name': 'Crear Transacción', 'url': None},
    ]

    return render(request, 'transacciones/crear.html', {'form': form, 'breadcrumbs': breadcrumbs})

@login_required
def ver_transacciones(request):
    transacciones = Transaccion.objects.all()
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Transacciones', 'url': None},
    ]
    return render(request, 'transacciones/ver.html', {'transacciones': transacciones, 'breadcrumbs': breadcrumbs})

@login_required
def registros_recientes(request):
    recientes = Transaccion.objects.all().order_by('-fecha')[:3]
    return render(request, 'transacciones/transacciones.html', {'recientes': recientes})

@login_required
def eliminar(request, id):
    transaccion = Transaccion.objects.get(id=id)
    transaccion.delete()
    return redirect('ver_transacciones')

@login_required
def search(request):
    search_type = request.GET.get('type')
    query = request.GET.get('query')

    if search_type == 'fecha':
        transacciones = Transaccion.objects.filter(fecha__icontains=query)
    elif search_type == 'descripcion':
        transacciones = Transaccion.objects.filter(descripcion__icontains=query)
    else:
        transacciones = Transaccion.objects.all()

    results = list(transacciones.values('tipo', 'descripcion', 'monto', 'fecha'))
    return JsonResponse(results, safe=False)

@login_required
def agregar_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo agregado exitosamente.')
            return redirect('agregar_insumo')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = InsumoForm()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Insumos', 'url': '/consultar_insumo/'},
        {'name': 'Agregar Insumo', 'url': None},
    ]

    return render(request, 'insumos/agregar_insumo.html', {'form': form, 'breadcrumbs': breadcrumbs})

@login_required
def editar_insumo(request):
    insumos = Insumo.objects.all()
    form = None

    if request.method == 'POST':
        original_nombre = request.POST.get('original-nombre')
        nombre = request.POST.get('nombre')
        insumo = Insumo.objects.filter(nombre=original_nombre).first()

        if insumo:
            form = InsumoForm(request.POST, instance=insumo)
            if form.is_valid():
                if Insumo.objects.filter(nombre=nombre).exclude(pk=insumo.pk).exists():
                    return render(request, 'insumos/editar_insumo.html', {'form': form, 'insumos': insumos})
                form.save()
                messages.success(request, 'Insumo actualizado exitosamente.')
                return redirect('consultar_insumo')
        else:
            messages.error(request, 'Insumo no encontrado.')
            return render(request, 'insumos/editar_insumo.html', {'form': form, 'insumos': insumos})
    else:
        nombre = request.GET.get('nombre')
        if nombre:
            insumo = Insumo.objects.filter(nombre=nombre).first()
            if insumo:
                form = InsumoForm(instance=insumo)
            else:
                messages.error(request, 'Insumo no encontrado.')
                return render(request, 'insumos/editar_insumo.html', {'insumos': insumos})

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Insumos', 'url': '/consultar_insumo/'},
        {'name': 'Editar Insumo', 'url': None},
    ]

    return render(request, 'insumos/editar_insumo.html', {'form': form, 'insumos': insumos, 'breadcrumbs': breadcrumbs})

@login_required
def verificar_nombre_insumo(request):
    nombre = request.GET.get('nombre', None)
    exists = Insumo.objects.filter(nombre=nombre).exists()
    return JsonResponse({'exists': exists})

@login_required
def eliminar_insumo(request, id):
    insumo = Insumo.objects.get(id=id)
    insumo.delete()
    return redirect('consultar_insumo')

@login_required
def consultar_insumo(request):
    query = request.GET.get('q', '')
    if query:
        insumos = Insumo.objects.filter(nombre__icontains=query)
    else:
        insumos = Insumo.objects.all()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Insumos', 'url': None},
    ]

    return render(request, 'insumos/consultar_insumo.html', {'insumos': insumos, 'breadcrumbs': breadcrumbs})

@login_required
def backup_view(request):
    if request.method == 'POST':
        if 'create_backup' in request.POST:
            backup = create_backup()
            if backup:
                messages.success(request, 'Copia de seguridad creada exitosamente.')
            else:
                messages.error(request, 'Error al crear la copia de seguridad.')
        elif 'restore_backup' in request.POST:
            backup_id = request.POST.get('backup_id')
            if restore_backup(backup_id):
                messages.success(request, 'Base de datos restaurada exitosamente.')
            else:
                messages.error(request, 'Error al restaurar la base de datos.')
        elif 'delete_backup' in request.POST:
            backup_id = request.POST.get('backup_id')
            backup = Backup.objects.get(id=backup_id)
            backup.delete()
            messages.success(request, 'Copia de seguridad eliminada exitosamente.')

    backups = Backup.objects.all().order_by('-created_at')
    
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Copia de Seguridad', 'url': None},
    ]
    
    return render(request, 'backup_restore/backup.html', {'backups': backups, 'breadcrumbs': breadcrumbs})


def download_backup(request, id):
    backup = get_object_or_404(Backup, id=id)
    response = HttpResponse(backup.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{backup.file.name}"'
    return response
