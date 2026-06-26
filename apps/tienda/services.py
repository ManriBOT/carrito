from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from .models import Carrito, CarritoItem, Producto, PerfilUsuario


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


def crear_producto(nombre, talla, color, descripcion, precio, activo=True):
    return Producto.objects.create(
        nombre=nombre,
        talla=talla,
        color=color,
        descripcion=descripcion,
        precio=precio,
        activo=activo
    )


def editar_producto(producto_id, **datos):
    producto = get_object_or_404(Producto, id=producto_id)
    for campo, valor in datos.items():
        if hasattr(producto, campo):
            setattr(producto, campo, valor)
    producto.save()
    return producto


def eliminar_producto(producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()


def obtener_todos_productos(incluir_inactivos=False):
    queryset = Producto.objects.all()
    if not incluir_inactivos:
        queryset = queryset.filter(activo=True)
    return queryset.order_by('-creado')


def obtener_producto(producto_id):
    return get_object_or_404(Producto, id=producto_id)


def crear_usuario(username, email, password, first_name='', last_name='', rol='usuario'):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    PerfilUsuario.objects.update_or_create(user=user, defaults={'rol': rol})
    grupo, _ = Group.objects.get_or_create(name=rol)
    user.groups.add(grupo)
    return user


def editar_usuario(user_id, **datos):
    user = get_object_or_404(User, id=user_id)
    perfil_data = {}
    if 'rol' in datos:
        perfil_data['rol'] = datos.pop('rol')
    if 'telefono' in datos:
        perfil_data['telefono'] = datos.pop('telefono')
    if 'direccion' in datos:
        perfil_data['direccion'] = datos.pop('direccion')
    if 'fecha_nacimiento' in datos:
        perfil_data['fecha_nacimiento'] = datos.pop('fecha_nacimiento')

    for campo, valor in datos.items():
        if hasattr(user, campo):
            setattr(user, campo, valor)
    user.save()

    if perfil_data:
        PerfilUsuario.objects.update_or_create(user=user, defaults=perfil_data)
        if 'rol' in perfil_data:
            Group.objects.filter(user=user).delete()
            grupo, _ = Group.objects.get_or_create(name=perfil_data['rol'])
            user.groups.add(grupo)
    return user


def eliminar_usuario(user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()


def obtener_todos_usuarios():
    return User.objects.select_related('perfil').all().order_by('-date_joined')
