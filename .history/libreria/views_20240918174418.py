from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Transaccion, Insumo, CustomUser, Backup
from django.contrib.auth.decorators import login_required
from .forms import InsumoForm, TransaccionForm, CustomUserCreationForm, LoginForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from .utils import create_backup, restore_backup
import os
from .forms import CustomPasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
@login_required
def inicio(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio'},
    ]
    return render(request, 'index/index.html', {'breadcrumbs': breadcrumbs})

@login_required
def usuario(request):
    usuario = request.user  # Obtiene el usuario actual que ha iniciado sesión
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuario', 'url': usuario},
    ]
    return render(request, 'usuario/usuario.html', {'usuario': usuario,'breadcrumbs': breadcrumbs})
@login_required
def manual(request):
    return render(request,'manual/Manual de ususario.pdf' )
@login_required
def contabilidad(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': 'Contabilidad', 'url': '/contabilidad'},
    ]
    return render(request, 'transacciones/transacciones.html', {'breadcrumbs': breadcrumbs})

@login_required
def insumos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': 'Gestión de insumos', 'url': '/insumos'},
    ]
    return render(request, 'insumos/insumos.html',{'breadcrumbs': breadcrumbs})

@login_required
def ver_perfil(request):
    usuario = request.user  # Obtiene el usuario actual que ha iniciado sesión

    if usuario.role == 'Empleado':
        if request.method == 'POST':
            admin_password = request.POST.get('admin_password')
            try:
                admin_user = CustomUser.objects.get(role='Administrador')
                if check_password(admin_password, admin_user.password):
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Contraseña incorrecta.'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No hay un usuario administrador registrado.'})
        
        return render(request, 'usuario/ver.html', {'usuario': usuario})

    # Si el usuario no es un empleado, simplemente mostrar la página del perfil
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Ver Perfil', 'url': '/ver_perfil'},
    ]
    return render(request, 'usuario/ver.html', {'usuario': usuario, 'breadcrumbs': breadcrumbs})

@login_required
def editar_perfil(request):
    usuario = request.user  
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Listar Usuarios', 'url': '/listar_usuario/'},
        {'name': 'Editar Perfil', 'url': '/editar_perfil'},
    ]
    # Obtén el usuario actual
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuario')  # Redirige a una página de perfil o a donde prefieras
    else:
        form = CustomUserChangeForm(instance=usuario)
    
    return render(request, 'usuario/editar.html', {'form': form, 'breadcrumbs': breadcrumbs})

def cambiar_contraseña(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito. Puedes iniciar sesión con tu nueva contraseña.')
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            messages.error(request, 'Hubo un error al cambiar tu contraseña. Asegúrate de que la contraseña actual sea correcta y que las nuevas contraseñas coincidan.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'usuario/usuario.html', {'form': form})

@login_required
def listar_usuario(request):
    usuarios = CustomUser.objects.filter(role='Empleado')  # Filtra por rol 'Empleado'
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Listar Usuarios', 'url': '/listar_usuario/'},
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
                if user.is_active:  # Verificar si el usuario está activo
                    auth_login(request, user)
                    
                    return redirect('inicio')  # Redirige a la página principal o a otra página
                else:
                    messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
            else:
                messages.error(request, 'Nombre o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  # Redirige a la página de inicio de sesión u otra página deseada


def crear_perfil(request):
    if request.method == 'POST':
        # Si el usuario es un empleado, pedir la contraseña del administrador
        if request.user.role == 'Empleado':
            admin_password = request.POST.get('admin_password')
            try:
                admin_user = User.objects.get(role='Administrador')
                if check_password(admin_password, admin_user.password):
                    form = CustomUserCreationForm(request.POST, request.FILES)
                    if form.is_valid():
                        user = form.save()
                        messages.success(request, f'Usuario {user.email} creado exitosamente.')
                        return redirect('login')
                    else:
                        messages.error(request, 'Por favor corrige los errores a continuación.')
                else:
                    messages.error(request, 'Contraseña del administrador incorrecta.')
            except User.DoesNotExist:
                messages.error(request, 'No hay un usuario administrador registrado.')
        else:
            # Si el usuario es un administrador, mostrar el formulario directamente
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                messages.success(request, f'Usuario {user.email} creado exitosamente.')
                return redirect('login')
            else:
                messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomUserCreationForm()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/'},
        {'name': 'Usuario', 'url': '/usuario/'},
        {'name': 'Crear Perfil', 'url': '/crear_perfil'},
    ]

    return render(request, 'usuario/registro.html', {'form': form, 'breadcrumbs': breadcrumbs, 'user_role': request.user.role})
@login_required
def crear_transacciones(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            nueva_transaccion = form.save(commit=False)
            nueva_transaccion.save()
            messages.success(request, 'Transacción creada exitosamente.')
            return redirect('ver_transacciones')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = TransaccionForm()

    breadcrumbs = [
       {'name': 'Inicio', 'url': '/'},
        {'name': 'Contabilidad', 'url': '/contabilidad'},
        {'name': 'Crear transacciones', 'url': '/crear_transacciones'},
    ]

    return render(request, 'transacciones/crear.html', {'form': form, 'breadcrumbs': breadcrumbs})

@login_required
def ver_transacciones(request):
    transacciones = Transaccion.objects.all()
    breadcrumbs = [
         {'name': 'Inicio', 'url': '/'},
        {'name': 'Contabilidad', 'url': '/contabilidad'},
        {'name': 'Ver transacciones', 'url': '/ver_transacciones'},
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
            return redirect('consultar_insumo')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = InsumoForm()

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': 'Gestión de insumos', 'url': '/insumos'},
        {'name': 'Agregar insumos', 'url': '/agregar_insumo'},
    ]

    return render(request, 'insumos/agregar_insumo.html', {'form': form, 'breadcrumbs': breadcrumbs})

def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    form = None

    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            # Verificar si hay otro insumo con el mismo nombre
            if Insumo.objects.filter(nombre=form.cleaned_data['nombre']).exclude(pk=insumo.pk).exists():
                form.add_error('nombre', 'Ya existe un insumo con ese nombre.')
            else:
                form.save()
                messages.success(request, 'Insumo actualizado exitosamente.')
                return redirect('consultar_insumo')  # Redirige a la lista de insumos
    else:
        form = InsumoForm(instance=insumo)

    breadcrumbs = [
          {'name': 'Inicio', 'url': '/inicio'},
        {'name': 'Gestión de insumos', 'url': '/insumos'},
        {'name': 'Lista de insumos', 'url': '/consultar_insumo'},
        {'name': 'Editar insumos', 'url': '/editar_insumo'},
    ]

    return render(request, 'insumos/editar_insumo.html', {'form': form, 'breadcrumbs': breadcrumbs})
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
         {'name': 'Inicio', 'url': '/inicio'},
        {'name': 'Gestión de insumos', 'url': '/insumos'},
        {'name': 'Lista de insumos', 'url': '/consultar_insumo'},
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
        {'name': 'Copia de Seguridad', 'url': '/backup_view'},
    ]
    
    return render(request, 'backup_restore/backup.html', {'backups': backups, 'breadcrumbs': breadcrumbs})


def download_backup(request, id):
    backup = get_object_or_404(Backup, id=id)
    response = HttpResponse(backup.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{backup.file.name}"'
    return response



def cambiar_estado_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = 'is_active' in request.POST
        user.save()
        return redirect('listar_usuario')  # Redirige a la página que quiera
    
    
def clientes(request):
    return render(request, 'clientes/clientes.html')
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('lista_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})
