import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import RegistroForm, LoginForm, AgregarCarritoForm
from .services import (
    agregar_al_carrito,
    eliminar_item,
    vaciar_carrito,
    calcular_subtotal,
    obtener_carrito,
)
from .models import Producto


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogo')
    else:
        form = RegistroForm()
    return render(request, 'tienda/login.html', {'form': form, 'modo': 'registro'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = LoginForm()
    return render(request, 'tienda/login.html', {'form': form, 'modo': 'login'})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def catalogo_view(request):
    colores = ['Rojo', 'Blanco', 'Negro']
    tallas = ['S', 'M', 'L', 'XL']
    productos = []
    nombres_base = ['Camisa Clásica', 'Camisa Slim Fit', 'Camisa Oversize']
    for i, nombre in enumerate(nombres_base):
        producto, created = Producto.objects.get_or_create(
            nombre=nombre,
            defaults={
                'color': random.choice(colores),
                'talla': random.choice(tallas),
                'precio': round(random.uniform(15.0, 45.0), 2),
            },
        )
        if not created:
            producto.color = random.choice(colores)
            producto.talla = random.choice(tallas)
            producto.precio = round(random.uniform(15.0, 45.0), 2)
            producto.save()
        productos.append(producto)
    form = AgregarCarritoForm()
    return render(request, 'tienda/catalogo.html', {'productos': productos, 'form': form})


@login_required
@require_POST
def agregar_al_carrito_view(request):
    form = AgregarCarritoForm(request.POST)
    if form.is_valid():
        producto_id = form.cleaned_data['producto_id']
        cantidad = form.cleaned_data['cantidad']
        agregar_al_carrito(request.user, producto_id, cantidad)
        messages.success(request, 'Producto agregado al carrito.')
    else:
        messages.error(request, 'Error al agregar el producto.')
    return redirect('catalogo')


@login_required
def carrito_view(request):
    carrito = obtener_carrito(request.user)
    items = carrito.items.select_related('producto').all()
    subtotal = calcular_subtotal(request.user)
    return render(request, 'tienda/carrito.html', {'items': items, 'subtotal': subtotal})


@login_required
@require_POST
def eliminar_item_view(request, item_id):
    eliminar_item(request.user, item_id)
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')


@login_required
@require_POST
def vaciar_carrito_view(request):
    vaciar_carrito(request.user)
    messages.success(request, 'ACCION_VACIADO_EXITOSA')
    return redirect('carrito')
