from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone  # Cambia a timezone
from datetime import datetime

class Cliente(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('minorista', 'Minorista'),
        ('mayorista', 'Mayorista'),
    ]
    
    TIPO_DOCUMENTO_CHOICES = [
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Cédula de extranjería', 'Cédula de extranjería'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'Número de Identificación Tributaria (NIT)'),
    ]
    
    tipo_cliente = models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE_CHOICES,
        blank=False
    )
    
    tipo_documento = models.CharField(
    max_length=21,
    choices=TIPO_DOCUMENTO_CHOICES,
    blank=False,
    default='cedula_ciudadania'  # Define un valor por defecto aquí
)

    documento = models.BigIntegerField(blank=False, default=0)
    nombre = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    telefono = models.CharField(max_length=15, blank=False)
    direccion = models.CharField(max_length=255, null=True, blank=False)
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.nombre



class Backup(models.Model):
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=1024)  # Incrementado para permitir rutas más largas
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.file_name

class Producto(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('kilogramo', 'Kilogramo (kg)'),
        ('gramo', 'Gramo (g)'),
        ('litro', 'Litro (l)'),
        ('mililitro', 'Mililitro (ml)'),
        ('unidad', 'Unidad'),
    ]

    CATEGORIA_CHOICES = [
        ('leche', 'Leche'),
        ('queso', 'Queso'),
        ('yogurt', 'Yogurt'),
        ('mantequilla', 'Mantequilla'),
        ('crema', 'Crema'),
        ('otros', 'Otros'),
    ]

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, blank=False)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='otros')
    presentacion = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES, default='unidad')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    fecha_elaboracion = models.DateTimeField(default=timezone.now)  # Cambia aquí
    fecha_vencimiento = models.DateTimeField(default=timezone.now)  # Cambia aquí
    temperatura_conservacion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    lote = models.CharField(max_length=50, default='lote_default')

    def formatear_precio(self):
        return f"{self.precio:,.2f}".replace(",", ".")

    def __str__(self):
        return f'{self.nombre} - {self.codigo}'

class Proveedor(models.Model):
    nit = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    direccion = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Registrado por"
    )

    def formatear_nit(self):
        nit_str = str(self.nit).zfill(10)
        return f"{nit_str[:3]}.{nit_str[3:6]}.{nit_str[6:9]}-{nit_str[9]}"

    def __str__(self):
        return f"{self.nombre} - {self.formatear_nit()}"

class Insumo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="nombre")
    descripcion = models.CharField(max_length=20, verbose_name="Descripción")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="insumos", verbose_name="Proveedor", default=1)
    cantidad = models.IntegerField(verbose_name="Cantidad")

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('Compra', 'Compra'),
        ('Venta', 'Venta'),
        ('Gasto', 'Gasto'),
        ('Ingreso', 'Ingreso'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    monto = models.DecimalField(max_digits=10, decimal_places=3, default=100.00, verbose_name="Monto")
    fecha = models.DateField()

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - ${self.monto}"


    