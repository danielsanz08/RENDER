from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone  # Cambia a timezone
from datetime import datetime

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
    
    presentacion = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES, default='unidad')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)  # Este campo puede ser problemático
    stock = models.IntegerField(default=0)  # AGREGAR ESTE CAMPO PARA INVENTARIO
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    fecha_elaboracion = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField(default=timezone.now)
    temperatura_conservacion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    lote = models.CharField(max_length=50, default='lote_default')
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def formatear_precio(self):
        return f"{self.precio:,.2f}".replace(",", ".")

    def __str__(self):
        return f'{self.nombre} - {self.codigo}'

class Proveedor(models.Model):
    TIPO_PERSONA_CHOICES = [
        ('Persona Jurídica', 'Persona Jurídica'),
        ('Persona Natural', 'Persona Natural'),
    ]

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
    tipo_persona = models.CharField(
        max_length=16,
        choices=TIPO_PERSONA_CHOICES,
        default='natural',  # Puedes cambiar el valor predeterminado si lo deseas
        verbose_name="Tipo de Persona"
    )

    def formatear_nit(self):
        nit_str = str(self.nit).zfill(10)  # Asegura que el NIT tenga al menos 10 dígitos
        return f"{nit_str[:3]}.{nit_str[3:6]}.{nit_str[6:9]}-{nit_str[9]}"  # Formato: 000.000.000-0

    def __str__(self):
        return f"{self.nombre} - {self.formatear_nit()}"  # Muestra el nombre y el NIT formateado

class Insumo(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Kilogramo', 'Kilogramo (kg)'),
        ('Gramo', 'Gramo (g)'),
        ('Litro', 'Litro (l)'),
        ('Mililitro', 'Mililitro (ml)'),
        ('Unidad', 'Unidad'),
    ]
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    descripcion = models.CharField(max_length=20, verbose_name="Descripción")
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES, default='Unidad')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="insumos", verbose_name="Proveedor", default=1)
    cantidad = models.IntegerField(verbose_name="Cantidad")  # Este campo puede ser problemático
    stock = models.IntegerField(default=0)  # AGREGAR ESTE CAMPO PARA INVENTARIO
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    registrado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
from django.db import models
from datetime import date
class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('Compra', 'Compra'),
        ('Venta', 'Venta'),
        ('Gasto', 'Gasto'),
        ('Ingreso', 'Ingreso'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Relaciones opcionales
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, null=True, blank=True)
    # ELIMINAR: insumo = models.ForeignKey('Insumo', on_delete=models.SET_NULL, null=True, blank=True)
    
    descripcion = models.CharField(max_length=255)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha = models.DateField(default=date.today)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    # Almacenamos TODOS los productos/insumos como JSON para flexibilidad
    productos_json = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.tipo} - ${self.monto_total} - {self.fecha}"

    def obtener_items(self):
        """Retorna todos los items de la transacción"""
        return self.productos_json.get('items', [])
    
    def obtener_insumos(self):
        """Retorna solo los items de tipo 'insumo' de la transacción"""
        items = self.productos_json.get('items', [])
        # Filtramos los items donde 'tipo' es 'insumo'
        insumos = [item for item in items if item.get('tipo') == 'insumo']
        return insumos
    def actualizar_inventario(self):
        """Actualiza el inventario según el tipo de transacción"""
        items = self.obtener_items()
        
        for item in items:
            try:
                tipo_item = item.get('tipo')
                item_id = item.get('id')
                cantidad = item.get('cantidad', 0)
                
                if not all([tipo_item, item_id, cantidad]):
                    continue

                if tipo_item == 'producto_venta':
                    # VENTA: disminuir stock de productos
                    producto = Producto.objects.get(id=item_id)
                    if self.tipo == 'Venta':
                        producto.stock -= cantidad
                        producto.save()

                elif tipo_item == 'insumo':
                    if self.tipo == 'Compra':
                        # COMPRA: aumentar stock de insumos
                        insumo = Insumo.objects.get(id=item_id)
                        insumo.stock += cantidad
                        insumo.save()
                    elif self.tipo == 'Gasto':
                        # GASTO: disminuir stock de insumos
                        insumo = Insumo.objects.get(id=item_id)
                        insumo.stock -= cantidad
                        insumo.save()

                elif tipo_item == 'producto_obtenido':
                    if self.tipo == 'Gasto':
                        # GASTO: aumentar stock de productos obtenidos
                        producto = Producto.objects.get(id=item_id)
                        producto.stock += cantidad
                        producto.save()

            except (Producto.DoesNotExist, Insumo.DoesNotExist) as e:
                print(f"Error actualizando inventario: {e}")
                continue

    def get_detalle_items(self):
        """Retorna una lista formateada de los items para mostrar"""
        items = self.obtener_items()
        detalle = []
        
        for item in items:
            tipo = item.get('tipo', '')
            nombre = item.get('nombre', '')
            cantidad = item.get('cantidad', 0)
            precio = item.get('precio', 0)
            subtotal = item.get('subtotal', 0)
            
            if tipo == 'producto_venta':
                tipo_display = "Producto Vendido"
            elif tipo == 'insumo':
                tipo_display = "Insumo"
            elif tipo == 'producto_obtenido':
                tipo_display = "Producto Obtenido"
            else:
                tipo_display = tipo
            
            detalle.append({
                'tipo': tipo_display,
                'nombre': nombre,
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': subtotal
            })
        
        return detalle

    class Meta:
        ordering = ['-fecha', '-id']
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'