from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    OPCIONES_COLOR = [
        ('Rojo', 'Rojo'),
        ('Blanco', 'Blanco'),
        ('Negro', 'Negro'),
    ]
    OPCIONES_TALLA = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=OPCIONES_COLOR)
    talla = models.CharField(max_length=5, choices=OPCIONES_TALLA)
    descripcion = models.TextField(max_length=500, blank=True, default='')
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.nombre} - {self.color} / {self.talla}'


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'Carrito de {self.usuario.username}'


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Ítem del carrito'
        verbose_name_plural = 'Ítems del carrito'
        unique_together = ('carrito', 'producto')

    @property
    def subtotal(self):
        from decimal import Decimal
        return Decimal(str(self.cantidad)) * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre}'
