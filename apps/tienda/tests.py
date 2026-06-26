from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from apps.tienda.models import Producto, Carrito, CarritoItem
from apps.tienda.services import (
    obtener_carrito,
    agregar_al_carrito,
    calcular_subtotal,
    vaciar_carrito,
    eliminar_item,
)


class CarritoServicesTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='testuser', password='testpass123')
        self.producto = Producto.objects.create(
            nombre='Camisa Test',
            color='Rojo',
            talla='M',
            precio=Decimal('25.99'),
        )

    def test_obtener_carrito_crea_nuevo(self):
        carrito = obtener_carrito(self.usuario)
        self.assertIsNotNone(carrito)
        self.assertEqual(carrito.usuario, self.usuario)

    def test_obtener_carrito_existente(self):
        carrito1 = obtener_carrito(self.usuario)
        carrito2 = obtener_carrito(self.usuario)
        self.assertEqual(carrito1.id, carrito2.id)

    def test_agregar_al_carrito(self):
        item = agregar_al_carrito(self.usuario, self.producto.id, 2)
        self.assertEqual(item.cantidad, 2)
        self.assertEqual(item.producto, self.producto)

    def test_agregar_producto_existente_incrementa(self):
        agregar_al_carrito(self.usuario, self.producto.id, 1)
        item = agregar_al_carrito(self.usuario, self.producto.id, 3)
        self.assertEqual(item.cantidad, 4)

    def test_calcular_subtotal(self):
        agregar_al_carrito(self.usuario, self.producto.id, 3)
        subtotal = calcular_subtotal(self.usuario)
        self.assertEqual(subtotal, Decimal('77.97'))

    def test_vaciar_carrito(self):
        agregar_al_carrito(self.usuario, self.producto.id, 1)
        vaciar_carrito(self.usuario)
        carrito = obtener_carrito(self.usuario)
        self.assertEqual(carrito.items.count(), 0)

    def test_eliminar_item(self):
        item = agregar_al_carrito(self.usuario, self.producto.id, 1)
        eliminar_item(self.usuario, item.id)
        carrito = obtener_carrito(self.usuario)
        self.assertEqual(carrito.items.count(), 0)

    def test_subtotal_carrito_vacio_es_cero(self):
        subtotal = calcular_subtotal(self.usuario)
        self.assertEqual(subtotal, Decimal('0'))
