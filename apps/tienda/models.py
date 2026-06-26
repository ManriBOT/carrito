import re
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


def validar_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
        raise ValidationError('El nombre de usuario solo puede contener letras, números y guiones bajos (3-30 caracteres).')


def validar_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError('Formato de email inválido.')


def validar_password(password):
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('La contraseña debe contener al menos una mayúscula.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('La contraseña debe contener al menos una minúscula.')
    if not re.search(r'\d', password):
        raise ValidationError('La contraseña debe contener al menos un número.')


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

    nombre = models.CharField(max_length=100, validators=[validar_username])
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
        ordering = ['-creado']

    def __str__(self):
        return f'{self.nombre} - {self.color} / {self.talla}'

    def clean(self):
        super().clean()
        if self.precio < 0:
            raise ValidationError({'precio': 'El precio no puede ser negativo.'})


class PerfilUsuario(models.Model):
    ROLES = [
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    telefono = models.CharField(max_length=20, blank=True, default='')
    direccion = models.TextField(max_length=500, blank=True, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f'{self.user.username} - {self.get_rol_display()}'

    def es_admin(self):
        return self.rol == 'admin' or self.user.is_superuser

    def es_vendedor(self):
        return self.rol == 'vendedor' or self.user.is_superuser


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


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        perfil, _ = PerfilUsuario.objects.get_or_create(user=instance, defaults={'rol': 'usuario'})
        grupo_usuario, _ = Group.objects.get_or_create(name='usuario')
        instance.groups.add(grupo_usuario)
