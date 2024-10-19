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
        ('cedula de extranjeria', 'Cédula de extranjería'),
        ('pasaporte', 'Pasaporte'),
        ('nit', 'Número de Identificación Tributaria (NIT)'),
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
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Registrado por"
    )

    def __str__(self):
        return self.nombre
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone, role='Empleado', password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, role=role, estado=CustomUser.ACTIVE, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, role='Administrador', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, name, phone, role, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ACTIVE = 2
    DISABLED = 1

    ROLE_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    
    ESTADO_CHOICES = [
        (DISABLED, 'Desactivado'),
        (ACTIVE, 'Activo'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=ACTIVE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos del usuario',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'role']

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.estado = self.DISABLED
        self.save()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.estado = self.ACTIVE
        super().save(*args, **kwargs)

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
