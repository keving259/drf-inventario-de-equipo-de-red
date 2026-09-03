from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Dispositivo, Puerto
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

class DispositivoModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username = 'user',
            password = 'user'
        )
        self.dispositivo = Dispositivo.objects.create(
            nombre = "Router",
            tipo = Dispositivo.Tipo.ROUTER,
            marca = 'Cisco',
            modelo = "ISR4321",
            ip_gestion = '192.168.1.1',
            ubicacion = 'Rack 1',
            propietario = self.user
        )
        
    def test_tipo_choices_display(self):
        self.assertEqual(self.dispositivo.get_tipo_display(), 'Router')
        
    def test_relacion_propietario_dispositivos(self):
        self.assertEqual(self.user.dispositivos.count(), 1)
        self.assertIn(self.dispositivo, self.user.dispositivos.all())
        
    def test_ip_invalida_lanza_error_de_validacion(self):
        dispositivo_invalido = Dispositivo(
            nombre = 'Switch',
            tipo = Dispositivo.Tipo.SWITCH,
            marca = 'TP-Link',
            modelo = 'TL-SG108',
            ip_gestion = '999.999.999.999',
            ubicacion = 'Rack 2',
            propietario = self.user
        )
        with self.assertRaises(ValidationError):
            dispositivo_invalido.full_clean()

class PuertoModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user', 
            password='user'
        )
        self.dispositivo = Dispositivo.objects.create(
            nombre = 'Switch Core',
            tipo = Dispositivo.Tipo.SWITCH,
            marca = 'Cisco',
            modelo = 'C92OO',
            ip_gestion = '10.0.0.1',
            ubicacion = 'Rack 3',
            propietario = self.user
        )
        self.puerto = Puerto.objects.create(
            dispositivo = self.dispositivo,
            numero_puerto = 'Gi0/1',
            tipo = Puerto.Tipo.ETHERNET_GIGA,
            velocidad = '1000Mbps',
            estado = True
        )
    
    def test_relacion_dispositivo_puertos(self):
        self.assertEqual(self.dispositivo.puertos.count(), 1)
        
    def test_eliminar_dispositivo_elimina_puertos_cascada(self):
        self.dispositivo.delete()
        self.assertEqual(Puerto.objects.count(), 0)

class DispositivoPermissionsTest(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='admin', password='admin', is_staff=True)
        self.normal_user = User.objects.create_user(username='lector', password='lector', is_staff=False)
        self.list_url = reverse('dispositivos-list')
        
    def test_usuario_no_autenticado(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_usuario_normal(self):
        self.client.force_authenticate(user=self.normal_user)
    
    def test_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
                    'nombre' : "Router",
                    'tipo' : Dispositivo.Tipo.ROUTER,
                    'marca' : 'Cisco',
                    'modelo' : "ISR4321",
                    'ip_gestion' : '192.168.1.1',
                    'ubicacion' : 'Rack 1',
                    'propietario' : self.staff_user.id
                }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_login(self):
        response = self.client.post(reverse('login'), {'username':'admin', 'password':'admin'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response_get = self.client.get(self.list_url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)