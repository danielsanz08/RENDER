from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import Transaccion, User,Insumo
from django.contrib.auth.decorators import login_required
from .forms import InsumoForm, TramsaccionForm

# Create your views here.


def inicio(request):
    return render(request,'index/index.html' )
@login_required
def usuario(request):
    return render(request, 'usuario/usuario.html')

@login_required
def contabilidad(request):
    return render(request, 'paginas/finanza.html')
@login_required
def insumos(request):
    return render(request, 'insumos/insumos.html')


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
def eliminar (request, id):
    transaccione = Transaccion.objects.get(id=id)
    transaccione.delete()
    return redirect('ver_transacciones')
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

def buscar_usuario(request):
    query = request.GET.get('query', '')  # Obtiene el parámetro 'query' de la solicitud
    usuarios = User.objects.filter(username__icontains=query)  # Filtra los usuarios según el nombre de usuario
    return render(request, 'usuarios/buscar.html', {'usuarios': usuarios, 'query': query})  # Renderiza la plantilla con los usuarios encontrados

def agregar_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_insumo')
    else:
        form = InsumoForm()
    return render(request, 'insumos/agregar_insumo.html', {'form': form})

def editar_insumo(request):
    insumos = Insumo.objects.all()
    form = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        insumo = Insumo.objects.filter(nombre=nombre).first()

        if insumo:
            form = InsumoForm(request.POST, instance=insumo)
            if form.is_valid():
                form.save()
                return redirect('consultar_insumo')
        else:
            return render(request, 'insumos/editar_insumo.html', {'insumos': insumos})
    else:
        nombre = request.GET.get('nombre')
        if nombre:
            insumo = Insumo.objects.filter(nombre=nombre).first()
            if insumo:
                form = InsumoForm(instance=insumo)
            else:
                return render(request, 'insumos/editar_insumo.html', {'insumos': insumos})
    return render(request, 'insumos/editar_insumo.html', {'form': form, 'insumos': insumos})

def eliminar_insumo(request, id):
    insumos = Insumo.objects.get(id=id)
    insumos.delete()
    return redirect('consultar_insumo')

def consultar_insumo(request):
    query = request.GET.get('q', '')
    if query:
        insumos = Insumo.objects.filter(nombre__icontains=query)
    else:
        insumos = Insumo.objects.all()
    return render(request, 'insumos/consultar_insumo.html', {'insumos': insumos})