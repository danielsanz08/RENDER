from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from uuid import uuid4
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

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

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
    
    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CLIENTE_CHOICES)
    tipo_documento = models.CharField(max_length=21, choices=TIPO_DOCUMENTO_CHOICES, default='Cédula de ciudadanía')
    documento = models.BigIntegerField()
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255, null=True)
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre


class Backup(models.Model):
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=1024)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.file_name




class Proveedor(models.Model):
    TIPO_PERSONA_CHOICES = [
        ('Persona Jurídica', 'Persona Jurídica'),
        ('Persona Natural', 'Persona Natural'),
    ]

    nit = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_persona = models.CharField(max_length=16, choices=TIPO_PERSONA_CHOICES, default='Persona Natural')

    def formatear_nit(self):
        nit_str = str(self.nit).zfill(10)
        return f"{nit_str[:3]}.{nit_str[3:6]}.{nit_str[6:9]}-{nit_str[9]}"

    def __str__(self):
        return f"{self.nombre} - {self.formatear_nit()}"


class Insumo(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Kilogramo', 'Kilogramo (kg)'),
        ('Gramo', 'Gramo (g)'),
        ('Litro', 'Litro (l)'),
        ('Mililitro', 'Mililitro (ml)'),
        ('Unidad', 'Unidad'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255)
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES, default='Unidad')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="insumos")
    cantidad = models.IntegerField()
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre



class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('gasto', 'Gasto'),
        ('ingreso', 'Ingreso'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Enlaza con el modelo Producto
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el cliente
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField(null=True, blank=True)  # Se permite nulo y que quede en blanco
    monto = models.DecimalField(max_digits=15, decimal_places=2)  # Ajustado para decimal en lugar de IntegerField
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.producto.nombre} - {self.monto}'
