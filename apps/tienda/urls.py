from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('catalogo/agregar/', views.agregar_producto_view, name='agregar_producto'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/', views.agregar_al_carrito_view, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item_view, name='eliminar_item'),
    path('carrito/vaciar/', views.vaciar_carrito_view, name='vaciar_carrito'),
]
