from django.contrib import admin
from .models import Producto, Carrito, CarritoItem


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'talla', 'precio', 'activo')
    list_filter = ('color', 'talla', 'activo')
    search_fields = ('nombre',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado', 'actualizado')
    search_fields = ('usuario__username',)


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'precio_unitario')
    list_filter = ('carrito__usuario',)
