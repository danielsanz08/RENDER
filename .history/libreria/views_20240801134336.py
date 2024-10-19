from django.shortcuts import render
from .models import Transaccion

def inicio(request):
    # Obtener los últimos 3 registros de transacciones
    registros_recientes = Transaccion.objects.order_by('-fecha')[:3]
    return render(request, 'index/index.html', {'registros_recientes': registros_recientes})

def usuario(request):
    return render(request, 'usuario/usuario.html')

def contabilidad(request):
    return render(request, 'paginas/finanza.html')

def insumos(request):
    return render(request, 'paginas/insumos.html')

def ver_perfil(request):
    return render(request, 'usuario/ver.html')

def editar_perfil(request):
    return render(request, 'usuario/editar.html')

def cambiar_contraseña(request):
    return render(request, 'usuario/nueva_contraseña.html')

def login(request):
    return render(request, 'login/login.html')

def transacciones(request):
    transacciones = Transaccion.objects.all()
    return render(request, 'paginas/transacciones.html', {'transacciones': transacciones})