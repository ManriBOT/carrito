from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.tienda.models import Producto, CarritoItem


class FlujoCompletoTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_registro_redirige_a_login(self):
        resp = self.client.post('/register/', {
            'username': 'nuevousuario',
            'password1': 'Passw0rdSegura',
            'password2': 'Passw0rdSegura',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('/login/', resp.redirect_chain[0][0])
        user = User.objects.filter(username='nuevousuario').first()
        self.assertIsNotNone(user)

    def test_login_redirige_a_catalogo(self):
        User.objects.create_user(username='testuser', password='testpass123')
        resp = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('/catalogo/', resp.redirect_chain[0][0])
        self.assertTrue(resp.context['user'].is_authenticated)

    def test_catalogo_muestra_productos(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        resp = self.client.get('/catalogo/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('productos', resp.context)

    def test_agregar_producto_y_ver_en_catalogo(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        resp = self.client.post('/catalogo/agregar/', {
            'nombre': 'Camisa Test',
            'talla': 'L',
            'color': 'Negro',
            'descripcion': 'Descripcion de prueba',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        p = Producto.objects.filter(nombre='Camisa Test').first()
        self.assertIsNotNone(p)
        self.assertEqual(p.talla, 'L')
        self.assertEqual(p.color, 'Negro')
        self.assertEqual(p.descripcion, 'Descripcion de prueba')

    def test_agregar_al_carrito_y_ver_items(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        p = Producto.objects.create(nombre='Camisa', color='Rojo', talla='M')
        resp = self.client.post('/carrito/agregar/', {
            'producto_id': p.id,
            'cantidad': 3,
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        item = CarritoItem.objects.filter(producto=p).first()
        self.assertIsNotNone(item)
        self.assertEqual(item.cantidad, 3)
        resp2 = self.client.get('/carrito/')
        self.assertEqual(resp2.status_code, 200)

    def test_vaciar_carrito(self):
        from apps.tienda.services import obtener_carrito
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        p = Producto.objects.create(nombre='Camisa', color='Rojo', talla='M')
        carrito = obtener_carrito(user)
        CarritoItem.objects.create(
            carrito=carrito,
            producto=p,
            cantidad=1,
            precio_unitario=p.precio,
        )
        resp = self.client.post('/carrito/vaciar/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CarritoItem.objects.filter(carrito__usuario=user).count(), 0)

    def test_logout_cierra_sesion(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        resp = self.client.post('/logout/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('/login/', resp.redirect_chain[0][0])

    def test_login_credenciales_invalidas(self):
        resp = self.client.post('/login/', {
            'username': 'noexiste',
            'password': 'malpass',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['form'].is_valid())
