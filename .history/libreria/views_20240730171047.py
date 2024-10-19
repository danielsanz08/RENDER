from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaccion

# Create your views here.

def inicio(request):
    return render(request, 'login/login.html')

def index(request):
    return render(request,'index/index.html' )

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

def ver_transacciones(request):
    transacciones = Transaccion.objects.all()
    return render(request, 'transacciones/ver.html', {'transacciones':transacciones})

def crear_transacciones(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        descripcion = request.POST['descripcion']
        monto = request.POST['monto']
        fecha = request.POST['fecha']
        
        transaccion = Transaccion(tipo=tipo, descripcion=descripcion, monto=monto, fecha=fecha)
        transaccion.save()
        
        return redirect('ver_transacciones')  # Redirige a la vista para ver las transacciones

    return render(request, 'transacciones/crear.html')
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
