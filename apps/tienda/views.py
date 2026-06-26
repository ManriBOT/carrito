import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistroForm, LoginForm, AgregarCarritoForm, ProductoForm, ProductoFormEditar
from .decorators import rate_limit
from .services import (
    agregar_al_carrito,
    eliminar_item,
    vaciar_carrito,
    calcular_subtotal,
    obtener_carrito,
    crear_producto,
    editar_producto,
    eliminar_producto,
    obtener_todos_productos,
    obtener_producto,
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
    obtener_todos_usuarios,
)
from .models import Producto, PerfilUsuario


def es_admin(user):
    return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'admin')


def es_vendedor(user):
    return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol in ['admin', 'vendedor'])


@rate_limit(max_attempts=5, window=300)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido a RED ESTAMPACION.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'tienda/login.html', {'form': form, 'modo': 'registro'})


@rate_limit(max_attempts=5, window=300)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            return redirect('catalogo')
    else:
        form = LoginForm()
    return render(request, 'tienda/login.html', {'form': form, 'modo': 'login'})


@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required
def catalogo_view(request):
    productos = obtener_todos_productos()
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
        form.save()
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
    messages.success(request, 'Carrito vaciado exitosamente.')
    return redirect('carrito')


# CRUD Productos
@login_required
@user_passes_test(es_vendedor)
def producto_editar_view(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoFormEditar(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('catalogo')
    else:
        form = ProductoFormEditar(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form, 'producto': producto, 'accion': 'editar'})


@login_required
@user_passes_test(es_vendedor)
@require_POST
def producto_eliminar_view(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
    return redirect('catalogo')


# CRUD Usuarios (Solo Admin)
@login_required
@user_passes_test(es_admin)
def usuarios_list_view(request):
    busqueda = request.GET.get('q', '')
    usuarios = obtener_todos_usuarios()
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )
    return render(request, 'tienda/usuarios_list.html', {'usuarios': usuarios, 'busqueda': busqueda})


@login_required
@user_passes_test(es_admin)
def usuario_crear_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol = request.POST.get('rol', 'usuario')
            perfil = user.perfil
            perfil.rol = rol
            perfil.save()
            messages.success(request, f'Usuario "{user.username}" creado con rol {rol}.')
            return redirect('usuarios_list')
    else:
        form = RegistroForm()
    return render(request, 'tienda/usuario_form.html', {'form': form, 'accion': 'crear'})


@login_required
@user_passes_test(es_admin)
def usuario_editar_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rol = request.POST.get('rol')
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'

        usuario.username = username
        usuario.email = email
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.is_active = is_active
        usuario.is_staff = is_staff
        usuario.save()

        if hasattr(usuario, 'perfil'):
            usuario.perfil.rol = rol
            usuario.perfil.save()

        messages.success(request, f'Usuario "{usuario.username}" actualizado correctamente.')
        return redirect('usuarios_list')

    return render(request, 'tienda/usuario_form.html', {'usuario': usuario, 'accion': 'editar'})


@login_required
@user_passes_test(es_admin)
@require_POST
def usuario_eliminar_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
    else:
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username}" eliminado correctamente.')
    return redirect('usuarios_list')


@login_required
def perfil_view(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, 'tienda/perfil.html', {'perfil': perfil})


@login_required
def perfil_editar_view(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        perfil.telefono = request.POST.get('telefono', '')
        perfil.direccion = request.POST.get('direccion', '')
        fecha_nac = request.POST.get('fecha_nacimiento')
        if fecha_nac:
            perfil.fecha_nacimiento = fecha_nac
        perfil.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    return render(request, 'tienda/perfil_form.html', {'perfil': perfil})


# API para toast notifications
def get_messages_api(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        messages_list = []
        for message in messages.get_messages(request):
            messages_list.append({
                'level': message.tags,
                'message': str(message),
            })
        return JsonResponse({'messages': messages_list})
    return JsonResponse({'messages': []})
