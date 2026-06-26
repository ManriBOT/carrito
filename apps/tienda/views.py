from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from .forms import RegistroForm, LoginForm, AgregarCarritoForm, ProductoForm
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
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora inicia sesión.')
            return redirect('login')
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


@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def catalogo_view(request):
    productos = Producto.objects.filter(activo=True).order_by('-creado')
    form = AgregarCarritoForm()
    producto_form = ProductoForm()
    return render(request, 'tienda/catalogo.html', {
        'productos': productos,
        'form': form,
        'producto_form': producto_form,
    })


@login_required
@require_POST
def agregar_producto_view(request):
    form = ProductoForm(request.POST)
    if form.is_valid():
        producto = form.save(commit=False)
        producto.precio = 0
        producto.save()
        messages.success(request, 'Producto publicado en el catálogo.')
    else:
        messages.error(request, 'Error al publicar el producto. Revisa los campos.')
    return redirect('catalogo')


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
