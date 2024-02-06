from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from Users.serializers import UserSerializer  # Ajusta según tu estructura de carpetas

class TuVistaTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_creacion_usuario_exitosa(self):
        # Datos de prueba
        data = {
            'cedula': '123456789',
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Hace una solicitud POST a la vista
        response = self.client.post('/ruta_de_tu_vista/', data, format='json')

        # Verifica que la respuesta sea 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el usuario se haya creado correctamente en la base de datos
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_creacion_usuario_con_error_de_validacion(self):
        # Datos de prueba con error de validación (p.ej., cedula no solo números)
        data = {
            'cedula': 'abc',  # Valor no válido
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Hace una solicitud POST a la vista
        response = self.client.post('/ruta_de_tu_vista/', data, format='json')

        # Verifica que la respuesta sea 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verifica que el usuario no se haya creado en la base de datos
        self.assertFalse(User.objects.filter(username='testuser').exists())

    # Puedes agregar más casos de prueba según tus necesidades
