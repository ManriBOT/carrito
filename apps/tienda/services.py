from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Carrito, CarritoItem, Producto


def obtener_carrito(usuario):
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


def agregar_al_carrito(usuario, producto_id, cantidad=1):
    carrito = obtener_carrito(usuario)
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad, 'precio_unitario': producto.precio},
    )
    if not created:
        item.cantidad += cantidad
        item.save()
    return item


def eliminar_item(usuario, item_id):
    carrito = obtener_carrito(usuario)
    item = get_object_or_404(CarritoItem, id=item_id, carrito=carrito)
    item.delete()


def vaciar_carrito(usuario):
    carrito = obtener_carrito(usuario)
    items_eliminados, _ = carrito.items.all().delete()
    return items_eliminados


def calcular_subtotal(usuario):
    carrito = obtener_carrito(usuario)
    items = carrito.items.select_related('producto').all()
    subtotal = sum(
        Decimal(str(item.cantidad)) * item.precio_unitario
        for item in items
    )
    return subtotal
