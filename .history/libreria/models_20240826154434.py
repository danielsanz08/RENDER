from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group, Permission
from django.contrib.auth.models import BaseUserManager

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('Compra', 'Compra'),
        ('Venta', 'Venta'),
        ('Gasto', 'Gasto'),
        ('Ingreso', 'Ingreso'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    monto = models.DecimalField(max_digits=10, decimal_places=3, default=100.00, verbose_name="Monto")
    fecha = models.DateField()

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - ${self.monto}"

class Insumo(models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="nombre")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    cantidad = models.IntegerField(verbose_name="Cantidad")

    def _str_(self):
        return self.nombre
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone, role, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, phone, role, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    


    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=2)  # Default to 'Activo'
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'role']

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.estado = 1  # Establecer estado como "Desactivado"
        self.save()  # Guardar el cambio en el estado en lugar de eliminar el objeto

    def save(self, *args, **kwargs):
        # Si el objeto es nuevo, establece el estado como 'Activo' (2)
        if self.pk is None:
            self.estado = 2
        super().save(*args, **kwargs)  # Llama al método save del padre para guardar el objeto