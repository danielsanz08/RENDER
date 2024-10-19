from django.db import models

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
