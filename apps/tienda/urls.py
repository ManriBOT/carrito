from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('catalogo/agregar/', views.agregar_producto_view, name='agregar_producto'),
    path('catalogo/editar/<int:producto_id>/', views.producto_editar_view, name='producto_editar'),
    path('catalogo/eliminar/<int:producto_id>/', views.producto_eliminar_view, name='producto_eliminar'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/', views.agregar_al_carrito_view, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item_view, name='eliminar_item'),
    path('carrito/vaciar/', views.vaciar_carrito_view, name='vaciar_carrito'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.perfil_editar_view, name='perfil_editar'),
    path('usuarios/', views.usuarios_list_view, name='usuarios_list'),
    path('usuarios/crear/', views.usuario_crear_view, name='usuario_crear'),
    path('usuarios/editar/<int:user_id>/', views.usuario_editar_view, name='usuario_editar'),
    path('usuarios/eliminar/<int:user_id>/', views.usuario_eliminar_view, name='usuario_eliminar'),
    path('api/messages/', views.get_messages_api, name='api_messages'),
]
